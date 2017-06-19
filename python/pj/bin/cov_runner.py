"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: pj cov sub cmd entrence
"""

import os
import shutil
import subprocess
import pcom
import env_booter

LOG = pcom.gen_logger(__name__)

def run_cov(args):
    """to run cov sub cmd"""
    if args.cov_module and (args.cov_merge or args.cov_rpt or args.cov_verdi):
        ced, _ = env_booter.EnvBooter().module_env(args.cov_module)
        ef_str = ""
        for elf in pcom.find_iter(ced["MODULE_CONFIG"], "*.el"):
            ef_str += f"-elfile {elf} "
        cov_merge_vdb = f"{ced['COV_MERGE']}{os.sep}{ced['MODULE']}_merge.vdb"
        cd_str = f"cd {os.path.dirname(cov_merge_vdb)} && "
        cov_str = ""
        if args.cov_merge:
            vdb_lst = list(pcom.find_iter(ced["COV_CM"], "*.vdb", True))
            if not vdb_lst:
                raise Exception("no coverage data found")
            merge_lst_file = f"{ced['COV_MERGE']}{os.sep}merge_lst"
            os.makedirs(os.path.dirname(merge_lst_file), exist_ok=True)
            with open(merge_lst_file, "w") as mlf:
                for vdb_dir in vdb_lst:
                    mlf.write(f"{vdb_dir}{os.linesep}")
                    if os.path.isdir(cov_merge_vdb):
                        mlf.write(cov_merge_vdb)
            cov_str = (
                f"{cd_str} urg -full64 -f {merge_lst_file} -dbname "
                f"{os.path.basename(cov_merge_vdb)} -noreport {ef_str}")
            subprocess.run(cov_str, shell=True, check=True)
            for cc_dir in pcom.find_iter(ced["COV_CM"], "testdata", True):
                shutil.rmtree(cc_dir, ignore_errors=True)
        if args.cov_rpt:
            if not os.path.isdir(cov_merge_vdb):
                raise Exception(f"coverage merge dir {cov_merge_vdb} is NA")
            cov_str = f"{cd_str} urg -full64 -dir {cov_merge_vdb} {ef_str} -format both"
            subprocess.run(cov_str, shell=True)
        if args.cov_verdi:
            if not os.path.isdir(cov_merge_vdb):
                raise Exception(f"coverage merge dir {cov_merge_vdb} is NA")
            cov_str = f"{cd_str} verdi -cov -covdir {cov_merge_vdb} {ef_str} &"
            subprocess.run(cov_str, shell=True)
        LOG.info("running coverage of %s module done", args.cov_module)
    else:
        raise Exception("missing main arguments")
