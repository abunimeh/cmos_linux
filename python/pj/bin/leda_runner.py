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
        leda_cfg_file = f"{ced['FLOW_LEDA']}{os.sep}leda.cfg"
        leda_dic_cfg = os.path.abspath(os.path.expandvars(self.leda_dic["leda_cfg"]))
        if self.leda_dic["leda_cfg"]:
            if not os.path.isfile(leda_dic_cfg):
                raise Exception(f"the input cfg file  {leda_dic_cfg} is NA.")
            leda_cfg_file = leda_dic_cfg
        self.leda_cfg = leda_cfg = pcom.gen_cfg([leda_cfg_file])
        leda_dir = ced["FLOW_LEDA"]
        leda_log_dir = (
            f"{leda_dir}{os.sep}"
            f"{pcom.rd_cfg(leda_cfg, 'leda', 'log_directory_name', True)}")
        leda_log = (
            f"{leda_log_dir}{os.sep}"
            f"{pcom.rd_cfg(leda_cfg, 'leda', 'log_file_name', True)}")
        self.dir_dic = dir_dic = {
            "dir": leda_dir,
            "log_dir": leda_log_dir,
            "log": leda_log}
        self.flist_file = f"{leda_dir}{os.sep}leda.flist"
        self.leda_tcl = f"{dir_dic['dir']}{os.sep}leda.tcl"
    def cov_file2rulelst(self, ffile, nwd, nwd_lst, rule_lst):
        """recursive generate leda rule list"""
        nwd_lst.append(os.getcwd())
        os.chdir(nwd)
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
                    self.cov_file2rulelst(new_line, os.path.dirname(new_line), nwd_lst, rule_lst)
                else:
                    rule_lst.append(line)
        os.chdir(nwd_lst.pop())
    def gen_flist_file(self):
        """to generate leda flist file"""
        os.makedirs(self.dir_dic["dir"], exist_ok=True)
        os.makedirs(self.dir_dic["log_dir"], exist_ok=True)
        for leda_flist in self.leda_dic["leda_flist_lst"]:
            if not os.path.isfile(leda_flist):
                raise Exception(f"base flist file {leda_flist} is NA")
        d_lst, v_lst, vhdl_lst = filelst_gen.FilelstGen().gen_file_lst(
            self.leda_dic["leda_flist_lst"])
        with open(self.flist_file, "w") as flf:
            flf.write(os.linesep.join(v_lst+vhdl_lst+d_lst))
    def kick_off_leda(self):
        """to kick off main leda flow without gui"""
        with open(self.flist_file) as flf:
            with open(f"{self.dir_dic['dir']}{os.sep}leda_on_off_warning.log", "w") as lwf:
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
        bb_str = ""
        if self.leda_dic["leda_bb_flist_lst"]:
            bb_con = ""
            for leda_bb_flist in self.leda_dic["leda_bb_flist_lst"]:
                if not os.path.isfile(leda_bb_flist):
                    raise Exception(f"black box flist file {leda_bb_flist} is NA")
                with open(leda_bb_flist) as lcf:
                    bb_con += f"{lcf.read()}{os.linesep}"
            bb_flist_file = f"{self.dir_dic['dir']}{os.sep}leda_bb.flist"
            with open(bb_flist_file, "w") as lcf:
                lcf.write(bb_con)
            bb_str = f"-bbox_file {bb_flist_file} "
        leda_opts = " ".join(pcom.rd_cfg(self.leda_cfg, "leda", "opts"))
        leda_str = (
            f"cd {self.dir_dic['dir']} && "
            f"leda {leda_opts} -config {self.leda_tcl} "
            f"-f {self.flist_file} {bb_str} -top {self.leda_dic['leda_top']} "
            f"-log_dir {self.dir_dic['log_dir']} -l {self.dir_dic['log']}")
        with open(f"{self.dir_dic['dir']}{os.sep}leda_cmd", "w") as lcf:
            lcf.write(f"{leda_str}{os.linesep}")
        subprocess.run(leda_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    def proc_leda(self):
        """to process and kick off leda flow"""
        self.gen_flist_file()
        nwd_lst = []
        rule_lst = []
        if os.path.isfile(self.leda_tcl):
            shutil.copy(
                self.leda_tcl,
                f"{self.dir_dic['dir']}{os.sep}"
                f"leda_{self.ced['TIME'].strftime('%Y_%m_%d_%H_%M_%S')}.tcl")
        if self.leda_dic["leda_waiver"]:
            with open(self.leda_tcl, "w") as ltf:
                for flist in self.leda_dic["leda_waiver"]:
                    flist = os.path.abspath(os.path.expandvars(flist.strip()))
                    if not os.path.isfile(flist):
                        raise Exception(f"base flist file {flist} is NA")
                    self.cov_file2rulelst(
                        flist, os.path.dirname(flist), nwd_lst, rule_lst)
                    ltf.write(os.linesep.join(rule_lst))
        if self.leda_dic["leda_gen_log"]:
            if not os.path.isfile(self.flist_file):
                raise Exception(f"generated leda filelist {self.flist_file} is NA")
            self.kick_off_leda()
            leda_error_flg = False
            str_pat = re.compile("|".join([re.escape(cc) for cc in pcom.rd_cfg(
                self.leda_cfg, "leda", "error_string")]))
            with open(self.dir_dic["log"], errors="replace") as llf:
                with open(f"{self.dir_dic['log_dir']}{os.sep}leda_error.log", "w") as elf:
                    for line in llf:
                        line = line.strip()
                        if str_pat.search(line):
                            elf.write(f"{line}{os.linesep}")
                            leda_error_flg = True
            if leda_error_flg:
                LOG.warning("ERRORs raised in the process of leda")
        elif self.leda_dic["leda_gui"]:
            leda_str = (
                f"cd {self.dir_dic['dir']} && "
                f"leda +gui -config {self.leda_tcl} -l {self.dir_dic['log']}")
            subprocess.run(leda_str, shell=True)

def run_leda(args):
    """to run leda sub cmd"""
    if args.leda_gen_log and args.leda_flist_lst and args.leda_top or args.leda_gui:
        LedaProc(
            {"leda_gen_log": args.leda_gen_log,
             "leda_flist_lst": args.leda_flist_lst,
             "leda_top": args.leda_top,
             "leda_bb_flist_lst": args.leda_bb_flist_lst,
             "leda_cfg": args.leda_cfg_file,
             "leda_waiver": args.leda_waiver_flist,
             "leda_gui": args.leda_gui}).proc_leda()
    else:
        raise Exception("missing main arguments")
