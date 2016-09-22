# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: LogParser class for parsing uvm/verilog case logs

### modules
import pcom
import os
import re
import subprocess
import json
import db_conn

### classes
class REOpter(object):
    def __init__(self, re_str):
        self.re_str = re_str
    def match(self, re_pat):
        self.re_result = re_pat.match(self.re_str)
        return bool(self.re_result)
    def search(self, re_pat):
        self.re_result = re_pat.search(self.re_str)
        return bool(self.re_result)
    def group(self, i):
        return self.re_result.group(i)

class LogParser(object):
    def __init__(self, ced, cfg_dic, ngs_tup, LOG=None):
        self.LOG = LOG if LOG else pcom.gen_logger()
        self.ced = ced
        self.cfg_dic = cfg_dic
        self.name, self.group, self.seed = ngs_tup
        pass_str = r''
        cp_str = '|'.join(pcom.rd_cfg(
            cfg_dic['case'], self.name, 'pass_string'))
        fp_str = pass_str+'|'+cp_str if cp_str else pass_str
        self.p_pat = re.compile(fp_str)
        fail_str = (r'\b[Ee]rror\b|\bERROR\b|\*E\b|'
                    r'\bUVM_(ERROR|FATAL)\s+:\s+([^0\s]|0[^$])')
        cf_str = '|'.join(pcom.rd_cfg(
            cfg_dic['case'], self.name, 'fail_string'))
        ff_str = fail_str+'|'+cf_str if cf_str else fail_str
        self.f_pat = re.compile(ff_str)
        ignore_str = r'^$'
        ci_str = '|'.join(pcom.rd_cfg(
            cfg_dic['case'], self.name, 'ignore_string'))
        fi_str = ignore_str+'|'+ci_str if ci_str else ignore_str
        self.i_pat = re.compile(fi_str)
        finish_str = r'\$finish at simulation time\s+(\d+)'
        self.fin_pat = re.compile(finish_str)
        cpu_time_str = r'CPU [Tt]ime:\s+(\d+\.\d+)\s+(\w+)'
        self.ct_pat = re.compile(cpu_time_str)
        uvm_str = r'\+UVM_TESTNAME=(\w+)\s'
        self.uvm_pat = re.compile(uvm_str)
        self.dut_ana_log = os.path.join(
            ced['GROUP_DIR'], self.group, 'dut_ana.log')
        self.tb_ana_log = os.path.join(
            ced['GROUP_DIR'], self.group, 'tb_ana.log')
        self.elab_log = os.path.join(
            ced['GROUP_DIR'], self.group, 'elab.log')
        self.simu_log = os.path.join(
            ced['MODULE_OUTPUT'], self.name, self.seed, self.seed+'.log')
        self.dut_ana_error_lst = []
        self.tb_ana_error_lst = []
        self.elab_error_lst = []
        self.simu_error_lst = []
        proj_ini_ver = subprocess.run(
            'svn log ${PROJ_ROOT} --limit 1', shell=True, check=True,
            stdout=subprocess.PIPE).stdout.decode()
        proj_ver = re.search(r'---\n(r\d+)\s|\s', proj_ini_ver).group(1)
        module_name = self.ced['MODULE']+'___'+self.ced['PROJ_NAME']
        group_name = self.group+'___'+module_name
        case_name = self.name+'___'+group_name
        self.case_dic = {'pub_date': self.ced['TIME'],
                         'case_name': case_name,
                         'c_name': self.name,
                         'group_name': group_name,
                         'g_name': self.group,
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
        self.group_dic = {'dut_ana_log': self.dut_ana_log,
                          'dut_ana_status': 'NA',
                          'dut_ana_error': 'NA',
                          'tb_ana_log': self.tb_ana_log,
                          'tb_ana_status': 'NA',
                          'tb_ana_error': 'NA',
                          'elab_log': self.elab_log,
                          'elab_status': 'NA',
                          'elab_error': 'NA',
                          'comp_cpu_time': 'NA'}
    def add_case_db(self):
        conn = db_conn.gen_conn()
        c = conn.cursor()
        c.execute('insert into regr_user (name) values (%s) on conflict '
                  '(name) do nothing;', (self.case_dic['user_name'],))
        c.execute('insert into regr_proj (name) values (%s) on conflict '
                  '(name) do nothing;', (self.case_dic['proj_name'],))
        c.execute('insert into regr_module (name) values (%s) on conflict '
                  '(name) do nothing;', (self.case_dic['module_name'],))
        c.execute('insert into regr_group (name) values (%s) on conflict '
                  '(name) do nothing;', (self.case_dic['group_name'],))
        c.execute('insert into regr_case (name) values (%s) on conflict '
                  '(name) do nothing;', (self.case_dic['case_name'],))
        c.execute(
            'insert into regr_sim (pub_date, proj_cl, seed, dut_ana_log, '
            'dut_ana_status, dut_ana_error, tb_ana_log, tb_ana_status, '
            'tb_ana_error, elab_log, elab_status, elab_error, simu_log, '
            'simu_status, simu_error, comp_cpu_time, simu_cpu_time, '
            'simu_time, case_id, group_id, module_id, proj_id, user_id) '
            'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
            '%s, %s, %s, %s, %s, '
            '(select id from regr_case where name=%s), '
            '(select id from regr_group where name=%s), '
            '(select id from regr_module where name=%s), '
            '(select id from regr_proj where name=%s), '
            '(select id from regr_user where name=%s))', (
                self.case_dic['pub_date'], self.case_dic['proj_cl'],
                self.case_dic['seed'], self.case_dic['dut_ana_log'],
                self.case_dic['dut_ana_status'],
                self.case_dic['dut_ana_error'], self.case_dic['tb_ana_log'],
                self.case_dic['tb_ana_status'], self.case_dic['tb_ana_error'],
                self.case_dic['elab_log'], self.case_dic['elab_status'],
                self.case_dic['elab_error'], self.case_dic['simu_log'],
                self.case_dic['simu_status'], self.case_dic['simu_error'],
                self.case_dic['comp_cpu_time'], self.case_dic['simu_cpu_time'],
                self.case_dic['simu_time'], self.case_dic['case_name'],
                self.case_dic['group_name'], self.case_dic['module_name'],
                self.case_dic['proj_name'], self.case_dic['user_name']))
        conn.commit()
        c.close()
        conn.close()
    def parse_dut_ana_log(self):
        if not os.path.isfile(self.dut_ana_log):
            return
        with open(self.dut_ana_log) as f:
            for line in f:
                line = line.strip()
                m = REOpter(line)
                if m.search(self.i_pat):
                    continue
                elif m.search(self.f_pat):
                    self.dut_ana_error_lst.append(line)
        if self.dut_ana_error_lst:
            self.group_dic['dut_ana_status'] = 'failed'
            self.group_dic['dut_ana_error'] = os.linesep.join(
                self.dut_ana_error_lst)
        else:
            self.group_dic['dut_ana_status'] = 'passed'
        self.LOG.debug("parsing group {0} analysis log file {1} done"
                       "".format(self.group, self.dut_ana_log))
    def parse_tb_ana_log(self):
        if not os.path.isfile(self.tb_ana_log):
            return
        with open(self.tb_ana_log) as f:
            for line in f:
                line = line.strip()
                m = REOpter(line)
                if m.search(self.i_pat):
                    continue
                elif m.search(self.f_pat):
                    self.tb_ana_error_lst.append(line)
        if self.tb_ana_error_lst:
            self.group_dic['tb_ana_status'] = 'failed'
            self.group_dic['tb_ana_error'] = os.linesep.join(
                self.tb_ana_error_lst)
        else:
            self.group_dic['tb_ana_status'] = 'passed'
        self.LOG.debug("parsing group {0} analysis log file {1} done"
                       "".format(self.group, self.tb_ana_log))
    def parse_elab_log(self):
        if not os.path.isfile(self.elab_log):
            return
        with open(self.elab_log) as f:
            fin_flg = False
            for line in f:
                line = line.strip()
                m = REOpter(line)
                if m.search(self.i_pat):
                    continue
                elif m.search(self.f_pat):
                    self.elab_error_lst.append(line)
                elif m.match(self.ct_pat):
                    fin_flg = True
                    self.group_dic['comp_cpu_time'] = m.group(1)
        if self.elab_error_lst:
            self.group_dic['elab_status'] = 'failed'
            self.group_dic['elab_error'] = os.linesep.join(self.elab_error_lst)
        elif not fin_flg:
            self.group_dic['elab_status'] = 'pending'
        else:
            self.group_dic['elab_status'] = 'passed'
        self.LOG.debug("parsing group {0} elaboration log file {1} done"
                       "".format(self.group, self.elab_log))
    def parse_simu_log(self):
        if not os.path.isfile(self.simu_log):
            return
        with open(self.simu_log) as f:
            fin_flg = False
            uvm_flg = False
            pass_flg = False
            for line in f:
                line = line.strip()
                m = REOpter(line)
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
            self.case_dic['simu_error'] = os.linesep.join(self.simu_error_lst)
        elif not fin_flg:
            self.case_dic['simu_status'] = 'pending'
        elif uvm_flg:
            self.case_dic['simu_status'] = 'passed'
        elif pass_flg:
            self.case_dic['simu_status'] = 'passed'
        else:
            self.case_dic['simu_status'] = 'unknown'
        self.LOG.debug("parsing case {0} simulation log file {1} done"
                       "".format(self.name, self.simu_log))
    def parse_log(self):
        group_log_json = os.path.join(
            self.ced['GROUP_DIR'], self.group, 'group_log.json')
        ralog_mt = os.path.getmtime(self.dut_ana_log)
        talog_mt = os.path.getmtime(self.tb_ana_log)
        elog_mt = os.path.getmtime(self.elab_log)
        if os.path.isfile(group_log_json) and os.path.getmtime(
                group_log_json) > max(ralog_mt, talog_mt, elog_mt):
            with open(group_log_json) as jf:
                self.group_dic = json.load(jf)
        else:
            self.parse_dut_ana_log()
            self.parse_tb_ana_log()
            self.parse_elab_log()
            with open(group_log_json, 'w') as jf:
                json.dump(self.group_dic, jf)
        self.parse_simu_log()
        self.case_dic.update(self.group_dic)
        self.add_case_db()
        return self.case_dic
