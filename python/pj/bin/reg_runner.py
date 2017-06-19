"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: pj reg sub cmd entrence
"""

import subprocess
import pcom
import env_booter

LOG = pcom.gen_logger(__name__)

def run_reg(args):
    """to run reg sub cmd"""
    if args.reg_module and args.reg_gen:
        ced, cfg_dic = env_booter.EnvBooter().module_env(args.reg_module)
        tb_top = pcom.rd_cfg(cfg_dic["simv"], "DEFAULT", "tb_top", True, "test_top")
        reg_str_lst = []
        for reg_file in pcom.find_iter(ced["MODULE_REG"], "*.ralf"):
            reg_str_lst.append(f"ralgen -full64 -t {tb_top} -uvm -c F -a {reg_file} ")
        subprocess.run(" && ".join(reg_str_lst), shell=True)
    else:
        raise Exception("missing main arguments")
