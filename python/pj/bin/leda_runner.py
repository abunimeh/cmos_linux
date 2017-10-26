"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj leda sub cmd entrence
"""

import os
import re
import shutil
import subprocess
import pcom
import env_booter
import filelst_gen

LOG = pcom.gen_logger(__name__)

class LedaProc(object):
    """leda flow processor for pj"""
    def __init__(self, leda_dic):
        if not shutil.which("leda"):
            raise Exception("leda is not loaded")
        self.leda_dic = leda_dic
        self.ced, self.cfg_dic = ced, _ = env_booter.EnvBooter().boot_env()
        src_dir = (
            os.path.abspath(os.path.expandvars(leda_dic["leda_src"]))
            if leda_dic["leda_src"] else f"{ced['FLOW_LEDA']}{os.sep}src")
        leda_cfg_file = f"{src_dir}{os.sep}leda.cfg"
        if not os.path.isfile(leda_cfg_file):
            raise Exception(f"the leda cfg file {leda_cfg_file} is NA.")
        self.leda_cfg = pcom.gen_cfg([leda_cfg_file])
        leda_time_dir = (
            f"{ced['FLOW_LEDA']}{os.sep}{os.path.basename(src_dir)}__{leda_dic['leda_top']}__"
            f"{ced['TIME'].strftime('%Y_%m_%d_%H_%M_%S')}")
        self.df_dic = {
            "src_dir": src_dir, "time_dir": leda_time_dir,
            "log_dir": f"{leda_time_dir}{os.sep}leda_logs",
            "log": f"{leda_time_dir}{os.sep}leda_logs{os.sep}leda.log",
            "flist_file": f"{leda_time_dir}{os.sep}leda.flist",
            "tcl": f"{leda_time_dir}{os.sep}leda.tcl",
            "bbox_file": f"{src_dir}{os.sep}bbox_file",
            "rule_dir": f"{src_dir}{os.sep}leda_rule",
            "waiver_dir": f"{src_dir}{os.sep}leda_waiver"}
    def cov_file2rulelst(self, ffile, nwd_lst, rule_lst):
        """recursive generate leda rule list"""
        nwd_lst.append(os.getcwd())
        os.chdir(os.path.dirname(ffile))
        with open(ffile) as fff:
            for line in fff:
                line = line.strip()
                if not line:
                    continue
                line = os.path.expandvars(line)
                if "//" in line or "#" in line:
                    line = re.sub(r"(//|#).*$", "", line).strip()
                    if not line:
                        continue
                if line.startswith("-f "):
                    new_line = os.path.abspath(line[3:].strip())
                    if not os.path.isfile(new_line):
                        raise Exception(f"file line {line} in flist {fff} is NA")
                    self.cov_file2rulelst(new_line, nwd_lst, rule_lst)
                else:
                    rule_lst.append(line)
        os.chdir(nwd_lst.pop())
    def gen_flist_file(self):
        """to generate leda flist file"""
        os.makedirs(self.df_dic["log_dir"], exist_ok=True)
        for leda_flist in self.leda_dic["leda_flist_lst"]:
            if not os.path.isfile(leda_flist):
                raise Exception(f"base flist file {leda_flist} is NA")
        d_lst, v_lst, vhdl_lst = filelst_gen.FilelstGen().gen_file_lst(
            self.leda_dic["leda_flist_lst"])
        with open(self.df_dic["flist_file"], "w") as flf:
            flf.write(os.linesep.join(v_lst+vhdl_lst+d_lst))
    def kick_off_leda(self):
        """to kick off main leda flow without gui"""
        if not os.path.isfile(self.df_dic["flist_file"]):
            raise Exception(f"generated leda filelist {self.df_dic['flist_file']} is NA")
        with open(self.df_dic["flist_file"]) as flf:
            with open(f"{self.df_dic['time_dir']}{os.sep}leda_on_off_warning.log", "w") as lwf:
                for line in flf:
                    line = line.strip()
                    if line.startswith("+incdir"):
                        continue
                    if not os.path.isfile(line):
                        raise Exception(f"rtl file {line} is NA")
                    with open(line, errors="replace") as lvf:
                        vf_con = lvf.read()
                    if "leda off" in vf_con:
                        wline = f"leda off in file {line}"
                        LOG.warning(wline)
                        lwf.write(wline)
                    if "leda on" in vf_con:
                        wline = f"leda on in file {line}"
                        LOG.warning(wline)
                        lwf.write(wline)
        bb_str = f"-bbox_file {self.df_dic['bbox_file']}" if os.path.isfile(
            self.df_dic["bbox_file"]) else ""
        leda_opts = " ".join(pcom.rd_cfg(self.leda_cfg, "leda", "opts"))
        leda_str = (
            f"cd {self.df_dic['time_dir']} && "
            f"leda {leda_opts} -config {self.df_dic['tcl']} "
            f"-f {self.df_dic['flist_file']} {bb_str} -top {self.leda_dic['leda_top']} "
            f"-log_dir {self.df_dic['log_dir']} -l {self.df_dic['log']}")
        with open(f"{self.df_dic['time_dir']}{os.sep}leda_cmd", "w") as lcf:
            lcf.write(f"{leda_str}{os.linesep}")
        subprocess.run(leda_str, shell=True, stdout=subprocess.PIPE)
    def proc_leda(self):
        """to process and kick off leda flow"""
        if self.leda_dic["leda_gen_log"]:
            os.makedirs(self.df_dic["time_dir"], exist_ok=True)
            self.gen_flist_file()
            nwd_lst = []
            rule_lst = []
            for rule_file in pcom.find_iter(self.df_dic["rule_dir"], "*.tcl"):
                self.cov_file2rulelst(rule_file, nwd_lst, rule_lst)
            for waiver_file in pcom.find_iter(self.df_dic["waiver_dir"], "*.tcl"):
                self.cov_file2rulelst(waiver_file, nwd_lst, rule_lst)
            with open(self.df_dic["tcl"], "w") as ltf:
                ltf.write(os.linesep.join(rule_lst))
            self.kick_off_leda()
            shutil.copyfile(self.df_dic["log"], f"{self.ced['FLOW_LEDA']}{os.sep}leda_latest.log")
            leda_error_flg = False
            str_pat = re.compile("|".join([re.escape(cc) for cc in pcom.rd_cfg(
                self.leda_cfg, "leda", "error_string")]))
            with open(self.df_dic["log"], errors="replace") as llf:
                with open(f"{self.df_dic['log_dir']}{os.sep}leda_error.log", "w") as elf:
                    for line in llf:
                        line = line.strip()
                        if str_pat.search(line):
                            elf.write(f"{line}{os.linesep}")
                            leda_error_flg = True
            if leda_error_flg:
                LOG.warning("ERRORs raised in the process of leda")
        elif self.leda_dic["leda_gui"]:
            leda_dir = os.path.abspath(os.path.expandvars(self.leda_dic["leda_dir"]))
            if not os.path.isdir(leda_dir):
                raise Exception(f"leda GUI loaded dir {leda_dir} is NA")
            leda_str = (
                f"cd {leda_dir} && "
                f"leda +gui -config {leda_dir}{os.sep}leda.tcl "
                f"-l {leda_dir}{os.sep}leda_logs{os.sep}leda.log")
            subprocess.run(leda_str, shell=True)

def run_leda(args):
    """to run leda sub cmd"""
    if (args.leda_gen_log and args.leda_flist_lst and args.leda_top
            or args.leda_gui and args.leda_dir):
        LedaProc(
            {"leda_gen_log": args.leda_gen_log,
             "leda_flist_lst": args.leda_flist_lst,
             "leda_top": args.leda_top,
             "leda_src": args.leda_src,
             "leda_gui": args.leda_gui,
             "leda_dir": args.leda_dir}).proc_leda()
    else:
        raise Exception("missing main arguments")
