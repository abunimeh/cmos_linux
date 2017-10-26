"""
Author: Huan Chen @ CPU Verification Platform Group
Email: chenh@cpu.com.cn
Description: DcLogParser class for parsing dc related logs
"""

import os
import re
import collections
import datetime as dt
import requests
import pcom

LOG = pcom.gen_logger(__name__)
QOR = "DCRM_FINAL_QOR_REPORT"
TIMING = "DCRM_FINAL_TIMING_REPORT"
POWER = "DCRM_FINAL_POWER_REPORT"

class DcLogParser(object):
    """dc flow all log parser"""
    def  __init__(self, ced, dc_cfg_dic):
        self.ced = ced
        self.dc_cfg_dic = dc_cfg_dic
        rpt_dir = pcom.rd_cfg(dc_cfg_dic, "set_args", "REPORTS_DIR", True)
        self.pat_dic = {
            "warn_pat1": re.compile(r"(.*?):\s*(.*?):(\d+?):(.*)\s*\((.*)\)"),
            "warn_pat2": re.compile(r"(.*?):\s*(.*)\.(.*?):"),
            "warn_pat3": re.compile(r"(.*?):\s*(.*?)\/(.*)."),
            "we_pat": re.compile(r"(.*?):\s*(.*)\s*\((.*)\)"),
            "line_pat": re.compile(r"\((.*)\)"),
            "ct_pat": re.compile(r".*\(\s*([\.\d]*).*\)"),
            "slk_pat": re.compile(r"(.*?)\s*\(.*\)\s*(.*)"),
            "tpg_pat": re.compile(r"(.*?)\s*\'(.*)\'")}
        self.dc_dic = {
            "user": self.ced["USER_NAME"],
            "proj": self.ced["PROJ_NAME"],
            "design_name": pcom.rd_cfg(dc_cfg_dic, "base_args", "DESIGN_NAME", True),
            "run_time" : dt.datetime.timestamp(self.ced["TIME"]),
            "clk_freq": pcom.rd_cfg(dc_cfg_dic, "set_args", "clk_freq", True),
            "dc_log": {},
            "tm_rpt": collections.defaultdict(list),
            "qor_rpt": collections.defaultdict(dict),
            "pw_rpt": {},
            "rpt_dir": rpt_dir,
            "log_file": os.path.join(os.path.dirname(rpt_dir), "dc.log")}
    def proc_dc_warning(self, warn_dic, dlf, line):
        """to process dc warning type information"""
        mop = pcom.REOpter(line)
        if mop.match(self.pat_dic["warn_pat1"]):
            (ew_file, ew_line, ew_info, ew_type) = (
                mop.group(2), mop.group(3), mop.group(4), mop.group(5))
            warn_dic[ew_type].append([ew_file, ew_line, ew_info])
        elif mop.match(self.pat_dic["warn_pat2"]):
            ew_info, ew_type = mop.group(2), mop.group(3)
            if ew_type.strip() in ("Renaming file", ):
                for _ in range(3):
                    ew_info += f",{dlf.readline().strip()}"
                warn_dic[ew_type.strip()].append([None, None, ew_info])
        elif mop.match(self.pat_dic["warn_pat3"]):
            ew_type, ew_info = mop.group(2), mop.group(3)
            if ew_type.strip() in ("Duplicate library", ):
                warn_dic[ew_type.strip()].append([None, None, ew_info])
        elif mop.match(self.pat_dic["we_pat"]):
            ew_info, ew_type = mop.group(2), mop.group(3)
            warn_dic[ew_type].append([None, None, ew_info])
        else:
            while not self.pat_dic["line_pat"].search(line):
                new_line = dlf.readline().strip()
                line += f" {new_line}"
            mop = pcom.REOpter(line)
            if mop.match(self.pat_dic["we_pat"]):
                ew_info, ew_type = mop.group(2), mop.group(3)
                warn_dic[ew_type].append([None, None, ew_info])
            else:
                LOG.warning("WARNING condition not matched in line %s", line)
        return warn_dic
    def parse_dc_log(self):
        """to parse main dc log"""
        warn_dic = collections.defaultdict(list)
        error_dic = collections.defaultdict(list)
        with open(self.dc_dic["log_file"]) as dlf:
            for line in dlf:
                line = line.strip()
                mop = pcom.REOpter(line)
                if line.startswith("Stack trace"):
                    error_dic["tcrash"].append("stack overflow in tool crash")
                    break
                elif line.startswith("CPU usage"):
                    if mop.match(self.pat_dic["ct_pat"]):
                        self.dc_dic["cpu_usage"] = mop.group(1)
                elif line.startswith("Warning:"):
                    warn_dic = self.proc_dc_warning(warn_dic, dlf, line)
                elif line.startswith("Error:"):
                    if mop.match(self.pat_dic["we_pat"]):
                        ew_info, ew_type = mop.group(2), mop.group(3)
                        error_dic[ew_type].append(ew_info)
                    else:
                        mop = pcom.REOpter(f"{line} {dlf.readline().strip()}")
                        if mop.match(self.pat_dic["we_pat"]):
                            ew_info, ew_type = mop.group(2), mop.group(3)
                            error_dic[ew_type].append(ew_info)
                        else:
                            LOG.info("ERROR: condition not matched in line %s", line)
        if "cpu_usage" not in self.dc_dic:
            self.dc_dic["cpu_usage"] = "NA"
            self.dc_dic["status"] = "crash" if "tcrash" in error_dic else "running"
        else:
            self.dc_dic["status"] = "finished"
        self.dc_dic["dc_log"]["warning"] = warn_dic
        self.dc_dic["dc_log"]["error"] = error_dic
        self.dc_dic["dc_log"]["log_path"] = self.dc_dic["log_file"]
    def parse_dc_tm_rpt(self):
        """to parse dc timing log"""
        dc_tm_file = os.path.join(
            self.dc_dic["rpt_dir"], pcom.rd_cfg(self.dc_cfg_dic, "set_args", TIMING, True))
        if not os.path.isfile(dc_tm_file):
            return
        with open(dc_tm_file) as dtf:
            targ_flag = False
            for line in dtf:
                line = line.strip()
                mop = pcom.REOpter(line)
                if line.startswith("Startpoint:"):
                    targ_flag = True
                    targ_dic = {}
                if targ_flag:
                    line_lst = line.split(":")
                    if line_lst[0] in ("Startpoint", "Endpoint", "Path Group"):
                        targ_dic[line_lst[0]] = line_lst[1].strip()
                if line.startswith("slack "):
                    targ_flag = False
                    if mop.match(self.pat_dic["slk_pat"]):
                        if float(mop.group(2)) < 0:
                            targ_dic[mop.group(1)] = float(mop.group(2))
                            self.dc_dic["tm_rpt"]["timing"].append(targ_dic)
                    else:
                        LOG.info("%s condition not matched in line %s", mop.group(1), line)
        self.dc_dic["tm_rpt"]["log_path"] = dc_tm_file
    def parse_dc_qor_rpt(self):
        """to parse dc qor log"""
        dc_qor_file = os.path.join(
            self.dc_dic["rpt_dir"], pcom.rd_cfg(self.dc_cfg_dic, "set_args", QOR, True))
        if not os.path.isfile(dc_qor_file):
            return
        with open(dc_qor_file) as dqf:
            lines_str = dqf.read()
            for blk_str in lines_str.split("\n\n"):
                if "-----" not in blk_str or "in2" in blk_str or "2out" in blk_str:
                    continue
                items_lst = []
                for l_str in blk_str.split("\n"):
                    if "-----" in l_str or not l_str:
                        continue
                    if ":" in l_str:
                        str_lst = l_str.split(":")
                        items_lst.append({str_lst[0].strip():float(str_lst[1])})
                    else:
                        mop = pcom.REOpter(l_str.strip())
                        items_lst.append(
                            mop.group(2) if mop.match(self.pat_dic["tpg_pat"]) else l_str.strip())
                if items_lst:
                    for item_dic in items_lst[1:]:
                        for key, value in item_dic.items():
                            self.dc_dic["qor_rpt"][items_lst[0]][key] = value
        self.dc_dic["qor_rpt"]["log_path"] = dc_qor_file
    def parse_dc_pw_rpt(self):
        """to parse dc power log"""
        dc_pw_file = os.path.join(
            self.dc_dic["rpt_dir"], pcom.rd_cfg(self.dc_cfg_dic, "set_args", POWER, True))
        if not os.path.isfile(dc_pw_file):
            return
        with open(dc_pw_file) as dpf:
            for line in dpf:
                line = line.strip()
                if line.startswith("Operating Conditions:"):
                    self.dc_dic["pw_rpt"]["lib"] = line.split("Library:")[1].strip()
                if line.startswith("Total  "):
                    line_lst = re.split(r"\s+(?=\d|NA)", line)
                    if len(line_lst) == 5:
                        self.dc_dic["pw_rpt"]["internal_pw"] = line_lst[1]
                        self.dc_dic["pw_rpt"]["swithing_pw"] = line_lst[2]
                        self.dc_dic["pw_rpt"]["leakage_pw"] = line_lst[3]
                        self.dc_dic["pw_rpt"]["total_pw"] = line_lst[4]
                    else:
                        self.dc_dic["pw_rpt"]["internal_pw"] = "NA"
                        self.dc_dic["pw_rpt"]["swithing_pw"] = "NA"
                        self.dc_dic["pw_rpt"]["leakage_pw"] = "NA"
                        self.dc_dic["pw_rpt"]["total_pw"] = "NA"
        self.dc_dic["pw_rpt"]["log_path"] = dc_pw_file
    def parse_log(self):
        """top execution function"""
        if os.path.isfile(self.dc_dic["log_file"]):
            self.parse_dc_log()
            if self.dc_dic["status"] == "finished":
                self.parse_dc_tm_rpt()
                self.parse_dc_qor_rpt()
                self.parse_dc_pw_rpt()
            query_url = "http://172.51.13.205:8000/pj_app/dc/db_query/query_insert_case/"
            requests.post(query_url, json=self.dc_dic)
            return self.dc_dic
        else:
            LOG.info("No dc.log file, please check dc flow!")
