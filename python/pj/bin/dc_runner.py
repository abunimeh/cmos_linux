"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj dc sub cmd entrence
"""

import os
import shutil
import subprocess
import time
import pcom
import env_booter
import filelst_gen
import dc_log_parser
import tm_log_parser
import fm_runner

LOG = pcom.gen_logger(__name__)

class DCProc(object):
    """dc flow processor for pj"""
    def __init__(self, dc_dic):
        if not shutil.which("dc_shell"):
            raise Exception("dc is not loaded")
        self.ced, _ = ced, _ = env_booter.EnvBooter().boot_env()
        self.dc_dic = dc_dic
        dc_pre_str = "dct" if dc_dic["topo"] else "dc"
        self.src_dir = src_dir = (
            os.path.abspath(os.path.expandvars(self.dc_dic["src"]))
            if self.dc_dic["src"] else f"{ced['FLOW_DC']}{os.sep}src")
        self.dc_cfg_dic = dc_cfg_dic = pcom.gen_cfg([f"{src_dir}{os.sep}dc.cfg"])
        for base_key, base_value in self.dc_cfg_dic["base_args"].items():
            os.environ[base_key] = base_value
            self.ced[base_key] = base_value
        dc_time_dir = (
            f"{ced['FLOW_DC']}{os.sep}{dc_pre_str}_{os.path.basename(src_dir)}_"
            f"{dc_cfg_dic['base_args']['DESIGN_NAME']}_"
            f"{ced['TIME'].strftime('%Y_%m_%d_%H_%M_%S')}")
        dc_dic_dir = os.path.abspath(os.path.expandvars(self.dc_dic["dir"]))
        if self.dc_dic["dir"]:
            if not os.path.isdir(dc_dic_dir):
                raise Exception(f"the input dir {dc_dic_dir} is NA.")
            dc_time_dir = dc_dic_dir
        os.makedirs(dc_time_dir, exist_ok=True)
        self.dir_dic = {
            "dc_time_dir": dc_time_dir,
            "reports_dir": f"{dc_time_dir}{os.sep}reports",
            "results_dir": f"{dc_time_dir}{os.sep}results",
            "tcl_dir": f"{dc_time_dir}{os.sep}tcl"}
    def gen_dir_dic(self):
        """to updated dc cfg and generate dc info dic"""
        dc_flist = pcom.rd_cfg(self.dc_cfg_dic, "base_args", "DESIGN_FLIST")
        for flist in dc_flist:
            if not os.path.isfile(flist):
                raise Exception(f"base flist file {flist} is NA")
        _, verilog_lst, vhdl_lst = filelst_gen.FilelstGen().gen_file_lst(dc_flist)
        self.dc_cfg_dic["set_args"]["rtl_files"] = os.linesep.join(verilog_lst+vhdl_lst)
        os.makedirs(self.dir_dic["reports_dir"], exist_ok=True)
        os.makedirs(self.dir_dic["results_dir"], exist_ok=True)
        os.makedirs(self.dir_dic["tcl_dir"], exist_ok=True)
        self.dc_cfg_dic["set_args"]["REPORTS_DIR"] = self.dir_dic["reports_dir"]
        self.dc_cfg_dic["set_args"]["RESULTS_DIR"] = self.dir_dic["results_dir"]
        self.dc_cfg_dic["dc__tcl"]["DcTcl_DIR"] = self.dir_dic["tcl_dir"]
        self.dc_cfg_dic["dc__tcl"]["DT_DIR"] = self.dir_dic["dc_time_dir"]
    def proc_dc(self):
        """to process and kick off dc flow"""
        if self.dc_dic["gen_tcl"]:
            self.gen_dir_dic()
            LOG.info("generating the tcl&sdc files from templates")
            dc_temp_dir = f"{self.src_dir}{os.sep}dc_template"
            for tcl_name in self.dc_cfg_dic.sections():
                if tcl_name == "base_args" or tcl_name == "set_args":
                    pcom.ren_tempfile(
                        f"{dc_temp_dir}{os.sep}set_args.tcl",
                        f"{self.dir_dic['tcl_dir']}{os.sep}set_args.tcl",
                        {"base_arg_dic": self.dc_cfg_dic["base_args"],
                         "set_arg_dic": self.dc_cfg_dic["set_args"]})
                else:
                    tn_str = tcl_name.replace('__', '.')
                    pcom.ren_tempfile(
                        f"{dc_temp_dir}{os.sep}{tn_str}",
                        f"{self.dir_dic['tcl_dir']}{os.sep}{tn_str}",
                        {"dc_dic":self.dc_cfg_dic})
        if self.dc_dic["run"]:
            dc_topo_str = (
                f"cd {self.dir_dic['dc_time_dir']} && "
                f"dc_shell {'-topo' if self.dc_dic['topo'] else ''} "
                f"-f {self.dir_dic['tcl_dir']}{os.sep}dc.tcl "
                f"-output_log_file {self.dir_dic['dc_time_dir']}{os.sep}dc.log ")
            try:
                proc = subprocess.Popen(dc_topo_str, shell=True)
                while proc.poll() is None:
                    time.sleep(300)
                    dc_log_parser.DcLogParser(self.ced, self.dc_cfg_dic).parse_log()
                dc_log_parser.DcLogParser(self.ced, self.dc_cfg_dic).parse_log()
            except KeyboardInterrupt:
                dc_log_parser.DcLogParser(self.ced, self.dc_cfg_dic).parse_log()
                proc.kill()
            if self.dc_dic["tm_flg"]:
                tm_rpt = os.path.join(self.dir_dic["reports_dir"], pcom.rd_cfg(
                    self.dc_cfg_dic, "set_args", "DCRM_FINAL_TIMING_REPORT", True))
                tm_log_parser.TmParser(
                    {"dt_file": tm_rpt, "level": self.dc_dic["tm_level"]}).parse_tm_log()
            if self.dc_dic["formality"]:
                if not shutil.which("fm_shell"):
                    raise Exception("fm is not loaded")
                LOG.info("updating the fm_dic and running formality")
                fm_cfg_dic = pcom.gen_cfg([f"{self.src_dir}{os.sep}fm.cfg"])
                fm_cfg_dic["fm"]["imp_filelist"] = os.linesep.join(
                    pcom.find_iter(self.dir_dic["results_dir"], "*.syn.v"))
                fm_cfg_dic["fm"]["set_svf"] = os.linesep.join(
                    pcom.find_iter(self.dir_dic["results_dir"], "*.syn.svf"))
                fm_cfg_dic["fm"]["DESIGN_NAME"] = pcom.rd_cfg(
                    self.dc_cfg_dic, "base_args", "DESIGN_NAME", True)
                fm_cfg_dic["fm"]["ref_filelist"] = pcom.rd_cfg(
                    self.dc_cfg_dic, "set_args", "rtl_files", True)
                fm_cfg_dic["fm"]["fm_top_dir"] = self.dir_dic["dc_time_dir"]
                fm_cfg_dic["fm"]["fm_src_dir"] = self.src_dir
                fm_runner.proc_fm(self.ced, fm_cfg_dic)

def run_dc(args):
    """to run dc sub cmd"""
    if args.dc_gen_tcl or args.dc_dir:
        DCProc(
            {"gen_tcl": args.dc_gen_tcl,
             "dir": args.dc_dir,
             "run": args.dc_run,
             "topo": args.dc_topo,
             "src": args.dc_src,
             "tm_flg": args.dc_tm_flg,
             "tm_level": args.dc_tm_level,
             "formality": args.dc_formality}).proc_dc()
        LOG.info("running dc done")
    else:
        raise Exception("missing main arguments")
