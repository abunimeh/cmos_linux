"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj icc sub cmd entrence
"""

import os
import re
import shutil
import subprocess
import pcom
import env_booter

LOG = pcom.gen_logger(__name__)

class ICCProc(object):
    """icc flow processor for pj"""
    def __init__(self, icc_dic):
        if not shutil.which("icc_shell"):
            raise Exception("icc is not loaded")
        self.icc_dic = icc_dic
        ced, _ = env_booter.EnvBooter().boot_env()
        src_dir = (
            os.path.abspath(os.path.expandvars(self.icc_dic["src"])) if self.icc_dic["src"] else
            f"{ced['FLOW_ICC']}{os.sep}src")
        time_str = ced['TIME'].strftime('%Y_%m_%d_%H_%M_%S')
        icct_dir = f"{ced['FLOW_ICC']}{os.sep}icc_{os.path.basename(src_dir)}_{time_str}"
        icc_dic_dir = os.path.abspath(os.path.expandvars(self.icc_dic["dir"]))
        if self.icc_dic["dir"]:
            if not os.path.isdir(icc_dic_dir):
                raise Exception(f"the input dir {icc_dic_dir} is NA.")
            icct_dir = icc_dic_dir
        if not self.icc_dic["dir"]:
            shutil.copytree(src_dir, icct_dir)
        self.icc_cfg_dic = pcom.gen_cfg([f"{icct_dir}{os.sep}icc.cfg"])
        self.stage_lst = self.icc_cfg_dic.options("icc_stage")
        logs_dir = f"{icct_dir}{os.sep}logs"
        self.dir_f_dic = {
            "icct_dir": icct_dir,
            "src_dir": src_dir,
            "logs_dir": logs_dir,
            "err_rpt": f"{logs_dir}{os.sep}err.rpt",
            "warn_rpt": f"{logs_dir}{os.sep}warning_rpt",
            "time": time_str}
    def parse_icc_log(self, log_file):
        """to parse icc log file"""
        if not os.path.isfile(log_file):
            raise Exception(f"{log_file} is not existed")
        err_lst = []
        warn_lst = []
        f_pat = re.compile("|".join(
            [re.escape(cc) for cc in pcom.rd_cfg(self.icc_cfg_dic, "icc_string", "fail_string")]))
        w_pat = re.compile("|".join(
            [re.escape(cc) for cc in pcom.rd_cfg(self.icc_cfg_dic, "icc_string", "warn_string")]))
        i_pat = re.compile(
            (r"^$|"+"|".join([re.escape(cc) for cc in pcom.rd_cfg(
                self.icc_cfg_dic, "icc_string", "ignore_string")])).strip("|"))
        with open(log_file) as lgf:
            for line in lgf:
                line = line.strip()
                if i_pat.search(line):
                    continue
                if f_pat.search(line):
                    err_lst.append(line)
                elif w_pat.search(line):
                    warn_lst.append(line)
        if warn_lst:
            with open(self.dir_f_dic["warn_rpt"], "a") as warnf:
                warnf.write(f"{os.linesep*3}{log_file}{os.linesep}")
                for warn in warn_lst:
                    warnf.write(f"{warn}{os.linesep}")
        with open(self.dir_f_dic["err_rpt"], "w") as errf:
            if err_lst:
                errf.write(f"{log_file}{os.linesep}")
                for err in err_lst:
                    errf.write(f"{err}{os.linesep}")
                raise Exception(f"Errors generated")
            else:
                errf.write(f"Errors not found")
    def run_cmd(self, cur_stage_lst):
        """to excute icc sub cmd"""
        main_scripts_dir = f"{self.dir_f_dic['icct_dir']}{os.sep}scripts{os.sep}main_icc_scripts"
        for stage in cur_stage_lst:
            if stage not in self.stage_lst:
                raise Exception(f"stage {stage} you typed is not existed")
            tcl_path = f"{main_scripts_dir}{os.sep}{self.icc_cfg_dic['icc_stage'][stage]}"
            if not os.path.isfile(tcl_path):
                raise Exception(f"file {tcl_path} is not existed")
            icc_stage = os.path.splitext(self.icc_cfg_dic['icc_stage'][stage])[0]
            log_file = f"{self.dir_f_dic['logs_dir']}{os.sep}{icc_stage}.log"
            run_str = (
                f"cd {self.dir_f_dic['icct_dir']} && "
                f"icc_shell -f {tcl_path} -output_log_file {log_file}")
            icc_proc = subprocess.Popen(run_str, shell=True)
            try:
                icc_proc.communicate()
                self.parse_icc_log(log_file)
            except KeyboardInterrupt:
                icc_proc.kill()
    def proc_icc(self):
        """to process and kick off icc flow"""
        os.makedirs(self.dir_f_dic["logs_dir"], exist_ok=True)
        open(self.dir_f_dic["warn_rpt"], "w").close()
        if self.icc_dic["stage"]:
            icc_stage_lst = self.icc_dic["stage"]
            self.run_cmd(icc_stage_lst)
        elif self.icc_dic["s_stage"]:
            icc_stage_lst = self.stage_lst[self.stage_lst.index(self.icc_dic["s_stage"]):]
            self.run_cmd(icc_stage_lst)
        bak_dir = (
            f"{self.dir_f_dic['icct_dir']}{os.sep}"
            f"backup__{'__'.join(icc_stage_lst)}__{self.dir_f_dic['time']}")
        os.makedirs(bak_dir, exist_ok=True)
        for result_dir in ("outputs", "reports", "logs"):
            shutil.copytree(
                f"{self.dir_f_dic['icct_dir']}{os.sep}{result_dir}",
                f"{bak_dir}{os.sep}{result_dir}")
def run_icc(args):
    """to run icc sub cmd"""
    if args.icc_stage or args.icc_start_stage:
        ICCProc(
            {"stage": args.icc_stage,
             "s_stage": args.icc_start_stage,
             "src": args.icc_src,
             "dir": args.icc_time_dir}).proc_icc()
    else:
        raise Exception("missing main arguments")
