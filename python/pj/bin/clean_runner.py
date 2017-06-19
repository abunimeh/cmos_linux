"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: pj clean sub cmd entrence
"""

import os
import shutil
import subprocess
import pcom
import env_booter

LOG = pcom.gen_logger(__name__)

def rmtree(path_lst):
    """to remove dirs cleanly"""
    for path in path_lst:
        if path in os.getcwd():
            raise Exception(f"it is in dir {path}, please cd out from it since it will be cleaned")
    rm_rsp = input(f"{path_lst} will be cleaned {os.linesep}--> yes or no? ")
    if rm_rsp.strip() in ("yes", "y"):
        for path in path_lst:
            shutil.rmtree(path, ignore_errors=True)
            LOG.info("cleaning %s dir done", path)
    else:
        LOG.info("canceled")

def clean_module(args, module_name):
    """to clean verification module level dirs"""
    ced, _ = env_booter.EnvBooter().module_env(module_name)
    clean_lst = []
    if args.clean_case_lst:
        clean_lst.extend(
            [f"{ced['MODULE_OUTPUT']}{os.sep}{cc}" for cc in args.clean_case_lst if cc])
    if args.clean_case:
        for case_dir in pcom.find_iter(ced["MODULE_OUTPUT"], "*", True, True):
            base_case_dir = os.path.basename(case_dir)
            if not (base_case_dir.startswith("__") and base_case_dir.endswith("__")):
                clean_lst.append(case_dir)
    if args.clean_cov:
        clean_lst.append(ced["OUTPUT_COV"])
    if args.clean_output:
        clean_lst.append(ced["MODULE_OUTPUT"])
    if args.clean_tb:
        LOG.info(
            "CAUTION!!! you are reverting %s directory, in which all modified/private "
            "files/directories will be removed!!!", ced["MODULE_TB"])
        svn_tb_ver = pcom.gen_svn_ver(ced["MODULE_TB"])
        clean_lst.append(ced["MODULE_TB"])
    if args.clean_config:
        LOG.info(
            "CAUTION!!! you are reverting %s directory, in which all modified/private "
            "files/directories will be removed!!!", ced["MODULE_CONFIG"])
        svn_cfg_ver = pcom.gen_svn_ver(ced["MODULE_CONFIG"])
        clean_lst.append(ced["MODULE_CONFIG"])
    rmtree(clean_lst)
    if args.clean_tb:
        subprocess.run(
            f"svn up {ced['MODULE_TB']} -{svn_tb_ver}", shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if args.clean_config:
        subprocess.run(
            f"svn up {ced['MODULE_CONFIG']} -{svn_cfg_ver}", shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_clean(args):
    """to run clean sub cmd"""
    if args.clean_module:
        module_name = (
            args.clean_case_lst[0].split("__")[0]
            if not args.clean_module else args.clean_module)
        if not module_name:
            raise Exception(
                f"case {args.clean_case_lst[0]} is not in standard format <module__case>, "
                f"so module name must be specified")
        clean_module(args, module_name)
    else:
        raise Exception("missing main arguments")
