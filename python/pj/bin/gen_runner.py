"""
Author: Ningxin Yang @ CPU Verification Group
Email: yangnx@cpu.com.cn
Description: pj gen sub cmd entrence
"""

import os
import copy
import pcom
import env_booter

LOG = pcom.gen_logger(__name__)

class UVMGen(object):
    """gen uvm env"""
    def __init__(self, module, module_dir):
        self.module = module
        self.module_dir = module_dir
        self.ced, self.cfg_dic = env_booter.EnvBooter().boot_env()
        self.filter_lst = []
        self.base_dic = {
            "module_name": self.module,
            "agt_name_lst": []}
    def gen_data_struc(self):
        """to generate base_dic and filter_lst"""
        while True:
            agt_name = input(f"input agt name: ")
            LOG.info(f"agt name is {agt_name}")
            self.base_dic["agt_name_lst"].append(agt_name)
            if input("generate another agt?(yes/y or no/n): ") in ("no", "n"):
                break
        for opt in self.cfg_dic["proj"].options("gen_with"):
            self.base_dic[opt] = False
            if input(f"create {opt}?(yes/y or no/n): ") in ("yes", "y"):
                self.base_dic[opt] = True
                continue
            self.filter_lst.extend(pcom.rd_cfg(self.cfg_dic["proj"], "gen_with", opt))
    def proc_uvm_gen(self):
        """to generate module uvm env"""
        m_dir = self.module_dir if self.module_dir else self.ced["PROJ_VERIF"]
        module_path = os.path.expandvars(f"{m_dir}{os.sep}{self.module}")
        if os.path.isdir(module_path):
            raise Exception(f"module path you typed {module_path} has already existed")
        self.gen_data_struc()
        pj_gen_dir = f"{self.ced['SHARE_TEMPLATES']}{os.sep}pj_gen"
        if not os.path.isdir(pj_gen_dir):
            raise Exception(f"pj_gen dir {pj_gen_dir} is NA")
        for sub_dir in pcom.find_iter(pj_gen_dir, "*", dir_flg=True):
            dest_dir = sub_dir.replace(pj_gen_dir, module_path)
            os.makedirs(dest_dir, exist_ok=True)
            LOG.info(f"create a new {dest_dir} directory.")
        for temp_file in pcom.find_iter(pj_gen_dir, "*"):
            t_fn = os.path.basename(temp_file)
            if t_fn in self.filter_lst:
                continue
            LOG.info(f"template file is {t_fn}")
            tf_str = temp_file.replace(pj_gen_dir, module_path)
            blk_n = self.module if t_fn.startswith("_") else ""
            if t_fn in pcom.rd_cfg(self.cfg_dic["proj"], "gen_agt", "multiple"):
                mul_dic = copy.deepcopy(self.base_dic)
                del mul_dic["agt_name_lst"]
                for agt_name in self.base_dic["agt_name_lst"]:
                    mul_dic["agt_name"] = agt_name
                    pcom.ren_tempfile(
                        temp_file, tf_str.replace(t_fn, f"{blk_n}_{agt_name}{t_fn}"), mul_dic)
            else:
                pcom.ren_tempfile(
                    temp_file, tf_str.replace(t_fn, f"{blk_n}{t_fn}"), self.base_dic)
        LOG.info(f"module {self.module} uvm env generated")
def run_gen(args):
    """to run gen sub cmd"""
    if args.gen_module:
        UVMGen(args.gen_module, args.gen_module_dir).proc_uvm_gen()
    else:
        raise Exception("missing main arguments")
