# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: LogParser class for parsing uvm/verilog case logs

### modules
import pcom
import os
import re
import subprocess
import json
import requests
import datetime as dt

### classes
class LogParser(object):
    def __init__(self, LOG, ced, cfg_dic, cvs_tup):
        self.LOG = LOG if LOG else pcom.gen_logger()
        self.ced = ced
        self.cfg_dic = cfg_dic
        self.case, self.simv, self.seed = cvs_tup
        pass_str = r''
        cp_str = '|'.join(pcom.rd_cfg(
            cfg_dic['case'], self.case, 'pass_string'))
        fp_str = pass_str+'|'+cp_str if cp_str else pass_str
        self.p_pat = re.compile(fp_str)
        fail_str = (r'\b[Ee]rror\b|\bERROR\b|\*E\b|'
                    r'\bUVM_(ERROR|FATAL)\s*:\s*[1-9]\d*')
        cf_str = '|'.join(pcom.rd_cfg(
            cfg_dic['case'], self.case, 'fail_string'))
        ff_str = fail_str+'|'+cf_str if cf_str else fail_str
        self.f_pat = re.compile(ff_str)
        ignore_str = r'^$'
        ci_str = '|'.join(pcom.rd_cfg(
            cfg_dic['case'], self.case, 'ignore_string'))
        fi_str = ignore_str+'|'+ci_str if ci_str else ignore_str
        self.i_pat = re.compile(fi_str)
        finish_str = r'\$finish at simulation time\s+(\d+)'
        self.fin_pat = re.compile(finish_str)
        cpu_time_str = r'CPU [Tt]ime:\s+(\d+\.\d+)\s+(\w+)'
        self.ct_pat = re.compile(cpu_time_str)
        uvm_str = r'\+UVM_TESTNAME=(\w+)\s'
        self.uvm_pat = re.compile(uvm_str)
        self.dut_ana_log = os.path.join(
            ced['SIMV_DIR'], self.simv, 'dut_ana.log')
        self.tb_ana_log = os.path.join(
            ced['SIMV_DIR'], self.simv, 'tb_ana.log')
        self.elab_log = os.path.join(
            ced['SIMV_DIR'], self.simv, 'elab.log')
        self.simu_log = os.path.join(
            ced['MODULE_OUTPUT'], self.case, self.seed, self.seed+'.log')
        self.dut_ana_error_lst = []
        self.tb_ana_error_lst = []
        self.elab_error_lst = []
        self.simu_error_lst = []
        proj_ini_ver = subprocess.run(
            'svn log ${PROJ_ROOT} --limit 1', shell=True, check=True,
            stdout=subprocess.PIPE).stdout.decode()
        proj_ver = re.search(r'---\n(r\d+)\s|\s', proj_ini_ver).group(1)
        module_name = self.ced['MODULE']+'___'+self.ced['PROJ_NAME']
        simv_name = self.simv+'___'+module_name
        case_name = self.case+'___'+simv_name
        self.case_dic = {'pub_date': dt.datetime.timestamp(self.ced['TIME']),
                         'case_name': case_name,
                         'c_name': self.case,
                         'simv_name': simv_name,
                         'v_name': self.simv,
                         'module_name': module_name,
                         'm_name': self.ced['MODULE'],
                         'proj_name': self.ced['PROJ_NAME'],
                         'user_name': self.ced['USER_NAME'],
                         'proj_cl': proj_ver,
                         'seed': self.seed,
                         'simu_log': self.simu_log,
                         'simu_status': 'NA',
                         'simu_error': 'NA',
                         'simu_cpu_time': 'NA',
                         'simu_time': 'NA'}
        self.simv_dic = {'dut_ana_log': self.dut_ana_log,
                          'dut_ana_status': 'NA',
                          'dut_ana_error': 'NA',
                          'tb_ana_log': self.tb_ana_log,
                          'tb_ana_status': 'NA',
                          'tb_ana_error': 'NA',
                          'elab_log': self.elab_log,
                          'elab_status': 'NA',
                          'elab_error': 'NA',
                          'comp_cpu_time': 'NA'}
    def parse_dut_ana_log(self):
        if not os.path.isfile(self.dut_ana_log):
            return
        with open(self.dut_ana_log) as f:
            for line in f:
                line = line.strip()
                m = pcom.REOpter(line)
                if m.search(self.i_pat):
                    continue
                elif m.search(self.f_pat):
                    self.dut_ana_error_lst.append(line)
        if self.dut_ana_error_lst:
            self.simv_dic['dut_ana_status'] = 'failed'
            self.simv_dic['dut_ana_error'] = os.linesep.join(
                self.dut_ana_error_lst)[-1000:]
        else:
            self.simv_dic['dut_ana_status'] = 'passed'
        self.LOG.debug("parsing simv {0} analysis log file {1} done"
                       "".format(self.simv, self.dut_ana_log))
    def parse_tb_ana_log(self):
        if not os.path.isfile(self.tb_ana_log):
            return
        with open(self.tb_ana_log) as f:
            for line in f:
                line = line.strip()
                m = pcom.REOpter(line)
                if m.search(self.i_pat):
                    continue
                elif m.search(self.f_pat):
                    self.tb_ana_error_lst.append(line)
        if self.tb_ana_error_lst:
            self.simv_dic['tb_ana_status'] = 'failed'
            self.simv_dic['tb_ana_error'] = os.linesep.join(
                self.tb_ana_error_lst)[-1000:]
        else:
            self.simv_dic['tb_ana_status'] = 'passed'
        self.LOG.debug("parsing simv {0} analysis log file {1} done"
                       "".format(self.simv, self.tb_ana_log))
    def parse_elab_log(self):
        if not os.path.isfile(self.elab_log):
            return
        with open(self.elab_log) as f:
            fin_flg = False
            for line in f:
                line = line.strip()
                m = pcom.REOpter(line)
                if m.search(self.i_pat):
                    continue
                elif m.search(self.f_pat):
                    self.elab_error_lst.append(line)
                elif m.match(self.ct_pat):
                    fin_flg = True
                    self.simv_dic['comp_cpu_time'] = m.group(1)
        if self.elab_error_lst:
            self.simv_dic['elab_status'] = 'failed'
            self.simv_dic['elab_error'] = os.linesep.join(
                self.elab_error_lst)[-1000:]
        elif not fin_flg:
            self.simv_dic['elab_status'] = 'pending'
        else:
            self.simv_dic['elab_status'] = 'passed'
        self.LOG.debug("parsing simv {0} elaboration log file {1} done"
                       "".format(self.simv, self.elab_log))
    def parse_simu_log(self):
        if not os.path.isfile(self.simu_log):
            return
        with open(self.simu_log) as f:
            fin_flg = False
            uvm_flg = False
            pass_flg = False
            for line in f:
                line = line.strip()
                m = pcom.REOpter(line)
                if m.search(self.i_pat):
                    continue
                elif m.search(self.f_pat):
                    self.simu_error_lst.append(line)
                elif m.match(self.fin_pat):
                    fin_flg = True
                    self.case_dic['simu_time'] = m.group(1)
                elif m.match(self.ct_pat):
                    self.case_dic['simu_cpu_time'] = m.group(1)
                elif m.search(self.uvm_pat):
                    uvm_flg = True
                elif m.search(self.p_pat):
                    pass_flg = True
        if self.simu_error_lst:
            self.case_dic['simu_status'] = 'failed'
            self.case_dic['simu_error'] = os.linesep.join(
                self.simu_error_lst)[-1000:]
        elif not fin_flg:
            self.case_dic['simu_status'] = 'pending'
        elif uvm_flg:
            self.case_dic['simu_status'] = 'passed'
        elif pass_flg:
            self.case_dic['simu_status'] = 'passed'
        else:
            self.case_dic['simu_status'] = 'unknown'
        self.LOG.debug("parsing case {0} simulation log file {1} done"
                       "".format(self.case, self.simu_log))
    def parse_log(self):
        simv_log_json = os.path.join(
            self.ced['SIMV_DIR'], self.simv, 'simv_log.json')
        ralog_mt = os.path.getmtime(self.dut_ana_log)
        talog_mt = os.path.getmtime(self.tb_ana_log)
        elog_mt = os.path.getmtime(self.elab_log)
        if os.path.isfile(simv_log_json) and os.path.getmtime(
                simv_log_json) > max(ralog_mt, talog_mt, elog_mt):
            with open(simv_log_json) as jf:
                self.simv_dic = json.load(jf)
        else:
            self.parse_dut_ana_log()
            self.parse_tb_ana_log()
            self.parse_elab_log()
            with open(simv_log_json, 'w') as jf:
                json.dump(self.simv_dic, jf)
        self.parse_simu_log()
        self.case_dic.update(self.simv_dic)
        query_url = 'http://172.51.13.205:8000/regr/db_query/query_insert_case/'
        requests.post(query_url, json=self.case_dic)
        return self.case_dic
