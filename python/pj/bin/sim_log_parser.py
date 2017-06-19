"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: LogParser class for parsing uvm/verilog case logs
"""

import os
import re
import json
import datetime as dt
import subprocess
import requests
import pcom

LOG = pcom.gen_logger(__name__)

class LogParser(object):
    """simulation flow all log parser"""
    def __init__(self, ced, cfg_dic, cvsr_tup):
        self.ced = ced
        self.cfg_dic = cfg_dic
        self.cvsr_tup = cvsr_tup
        self.pat_dic = {
            "f_pat": re.compile(
                (r"\b[Ee]rror\b|\bERROR\b|\*E\b|\bUVM_(ERROR|FATAL)\s*:\s*[1-9]\d*|"+"|".join(
                    [re.escape(cc) for cc in pcom.rd_cfg(
                        cfg_dic["case"], cvsr_tup[0], "fail_string")])).strip("|")),
            "i_pat": re.compile(
                (r"^$|"+"|".join([re.escape(cc) for cc in pcom.rd_cfg(
                    cfg_dic["case"], cvsr_tup[0], "ignore_string")])).strip("|")),
            "ct_pat": re.compile(r"CPU [Tt]ime:\s+(\d*\.\d+)\s+(\w+)"),
            "p_pat": re.compile(
                (r"|"+"|".join([re.escape(cc) for cc in pcom.rd_cfg(
                    cfg_dic["case"], cvsr_tup[0], "pass_string")])).strip("|")),
            "fin_pat": re.compile(r"\$finish at simulation time\s+(\d+)"),
            "uvm_pat": re.compile(r"\+UVM_TESTNAME=(\w+)\s")}
        self.log_dic = log_dic = {
            "da": os.path.join(ced["OUTPUT_SIMV"], cvsr_tup[1], "dut_ana.log"),
            "ta": os.path.join(ced["OUTPUT_SIMV"], cvsr_tup[1], "tb_ana.log"),
            "e": os.path.join(ced["OUTPUT_SIMV"], cvsr_tup[1], "elab.log"),
            "s": os.path.join(
                ced["MODULE_OUTPUT"], cvsr_tup[0], cvsr_tup[2], f"{cvsr_tup[2]}.log")}
        module_name = f"{ced['MODULE']}___{ced['PROJ_NAME']}"
        simv_name = f"{cvsr_tup[1]}___{module_name}"
        case_name = f"{cvsr_tup[0]}___{simv_name}"
        try:
            svn_ver = pcom.gen_svn_ver(ced["PROJ_ROOT"])
        except subprocess.CalledProcessError:
            svn_ver = pcom.gen_svn_ver(ced["PROJ_VERIF"])
        self.sc_dic = {
            "s": {
                "dut_ana_log": log_dic["da"],
                "dut_ana_status": "NA",
                "dut_ana_error": "NA",
                "tb_ana_log": log_dic["ta"],
                "tb_ana_status": "NA",
                "tb_ana_error": "NA",
                "elab_log": log_dic["e"],
                "elab_status": "NA",
                "elab_error": "NA",
                "comp_cpu_time": "NA"},
            "c": {
                "pub_date": dt.datetime.timestamp(ced["TIME"]),
                "end_date": dt.datetime.timestamp(dt.datetime.now()),
                "case_name": case_name,
                "c_name": cvsr_tup[0],
                "simv_name": simv_name,
                "v_name": cvsr_tup[1],
                "module_name": module_name,
                "m_name": ced["MODULE"],
                "proj_name": ced["PROJ_NAME"],
                "user_name": ced["USER_NAME"],
                "proj_cl": svn_ver,
                "seed": cvsr_tup[2],
                "simu_log": log_dic["s"],
                "simu_status": "NA",
                "simu_error": "NA",
                "simu_cpu_time": "NA",
                "simu_time": "NA",
                "regr_types": cvsr_tup[3]}}
    def parse_dut_ana_log(self):
        """to parse dut log in analysis stage"""
        if not os.path.isfile(self.log_dic["da"]):
            return
        dut_ana_error_lst = []
        with open(self.log_dic["da"]) as daf:
            for line in daf:
                line = line.strip()
                mop = pcom.REOpter(line)
                if mop.search(self.pat_dic["i_pat"]):
                    continue
                elif mop.search(self.pat_dic["f_pat"]):
                    dut_ana_error_lst.append(line)
        if dut_ana_error_lst:
            self.sc_dic["s"]["dut_ana_status"] = "failed"
            self.sc_dic["s"]["dut_ana_error"] = os.linesep.join(dut_ana_error_lst)[-1000:]
        else:
            self.sc_dic["s"]["dut_ana_status"] = "passed"
        LOG.debug(
            "parsing simv %s dut analysis log file %s done", self.cvsr_tup[1], self.log_dic["da"])
    def parse_tb_ana_log(self):
        """to parse tb log in analysis stage"""
        if not os.path.isfile(self.log_dic["ta"]):
            return
        tb_ana_error_lst = []
        with open(self.log_dic["ta"]) as taf:
            for line in taf:
                line = line.strip()
                mop = pcom.REOpter(line)
                if mop.search(self.pat_dic["i_pat"]):
                    continue
                elif mop.search(self.pat_dic["f_pat"]):
                    tb_ana_error_lst.append(line)
        if tb_ana_error_lst:
            self.sc_dic["s"]["tb_ana_status"] = "failed"
            self.sc_dic["s"]["tb_ana_error"] = os.linesep.join(tb_ana_error_lst)[-1000:]
        else:
            self.sc_dic["s"]["tb_ana_status"] = "passed"
        LOG.debug(
            "parsing simv %s tb analysis log file %s done", self.cvsr_tup[1], self.log_dic["ta"])
    def parse_elab_log(self):
        """to parse log in elaboration stage"""
        if not os.path.isfile(self.log_dic["e"]):
            return
        elab_error_lst = []
        with open(self.log_dic["e"]) as elf:
            fin_flg = False
            for line in elf:
                line = line.strip()
                mop = pcom.REOpter(line)
                if mop.search(self.pat_dic["i_pat"]):
                    continue
                elif mop.search(self.pat_dic["f_pat"]):
                    elab_error_lst.append(line)
                elif mop.match(self.pat_dic["ct_pat"]):
                    fin_flg = True
                    self.sc_dic["s"]["comp_cpu_time"] = mop.group(1)
        if elab_error_lst:
            self.sc_dic["s"]["elab_status"] = "failed"
            self.sc_dic["s"]["elab_error"] = os.linesep.join(elab_error_lst)[-1000:]
        elif not fin_flg:
            self.sc_dic["s"]["elab_status"] = "pending"
        else:
            self.sc_dic["s"]["elab_status"] = "passed"
        LOG.debug(
            "parsing simv %s elaboration log file %s done", self.cvsr_tup[1], self.log_dic["e"])
    def parse_simu_log(self):
        """to parse log in simulation stage"""
        if not os.path.isfile(self.log_dic["s"]):
            return
        simu_error_lst = []
        with open(self.log_dic["s"]) as slf:
            fin_flg = False
            uvm_flg = False
            pass_flg = False
            for line in slf:
                line = line.strip()
                mop = pcom.REOpter(line)
                if mop.search(self.pat_dic["i_pat"]):
                    continue
                elif mop.search(self.pat_dic["f_pat"]):
                    simu_error_lst.append(line)
                elif mop.match(self.pat_dic["fin_pat"]):
                    fin_flg = True
                    self.sc_dic["c"]["simu_time"] = mop.group(1)
                elif mop.match(self.pat_dic["ct_pat"]):
                    self.sc_dic["c"]["simu_cpu_time"] = mop.group(1)
                elif mop.search(self.pat_dic["uvm_pat"]):
                    uvm_flg = True
                elif self.pat_dic["p_pat"].pattern and mop.search(self.pat_dic["p_pat"]):
                    pass_flg = True
        if simu_error_lst:
            self.sc_dic["c"]["simu_status"] = "failed"
            self.sc_dic["c"]["simu_error"] = os.linesep.join(simu_error_lst)[-1000:]
        elif not fin_flg:
            self.sc_dic["c"]["simu_status"] = "pending"
        elif uvm_flg or pass_flg:
            self.sc_dic["c"]["simu_status"] = "passed"
        else:
            self.sc_dic["c"]["simu_status"] = "unknown"
        LOG.debug(
            "parsing case %s simulation log file %s done", self.cvsr_tup[0], self.log_dic["s"])
    def proc_pass_flg_file(self):
        """to process case pass flag file according to simulation status"""
        pass_flg_file = f"{os.path.dirname(self.log_dic['s'])}{os.sep}case_passed"
        if self.sc_dic["c"]["simu_status"] == "passed":
            open(pass_flg_file, "w").close()
        elif os.path.isfile(pass_flg_file):
            os.remove(pass_flg_file)
        LOG.debug("processing case pass flg file %s done", pass_flg_file)
    def parse_log(self):
        """top execution function"""
        simv_log_json = os.path.join(self.ced["OUTPUT_SIMV"], self.cvsr_tup[1], "simv_log.json")
        case_log_json = os.path.join(
            self.ced["MODULE_OUTPUT"], self.cvsr_tup[0], self.cvsr_tup[2], "case_log.json")
        dalog_mt = os.path.getmtime(self.log_dic["da"])
        talog_mt = os.path.getmtime(self.log_dic["ta"])
        elog_mt = os.path.getmtime(self.log_dic["e"])
        slog_mt = os.path.getmtime(self.log_dic["s"])
        if os.path.isfile(simv_log_json) and os.path.getmtime(
                simv_log_json) > max(dalog_mt, talog_mt, elog_mt):
            with open(simv_log_json) as sjf:
                self.sc_dic["s"] = json.load(sjf)
        else:
            self.parse_dut_ana_log()
            self.parse_tb_ana_log()
            self.parse_elab_log()
            with open(simv_log_json, "w") as sjf:
                json.dump(self.sc_dic["s"], sjf)
        if slog_mt < max(dalog_mt, talog_mt, elog_mt):
            self.sc_dic["c"]["simu_status"] = "unknown"
        else:
            self.parse_simu_log()
        with open(case_log_json, "w") as cjf:
            json.dump(self.sc_dic["c"], cjf)
        self.proc_pass_flg_file()
        fin_dic = {}
        fin_dic.update(self.sc_dic["s"])
        fin_dic.update(self.sc_dic["c"])
        query_url = "http://172.51.13.205:8000/pj_app/regr/db_query/query_insert_case/"
        requests.post(query_url, json=fin_dic)
        return fin_dic
