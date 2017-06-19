"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: pj ac sub cmd entrence
"""

import os
import shutil
import subprocess
import pcom

LOG = pcom.gen_logger(__name__)

def run_ac(args):
    """to run ac sub cmd"""
    if not shutil.which("emacs"):
        raise Exception("emacs is not loaded")
    if args.ac_dir:
        ac_dir = os.path.abspath(os.path.expandvars(args.ac_dir))
        if not os.path.isdir(ac_dir):
            raise Exception(f"auto connection directory {ac_dir} is NA")
        for ac_file in pcom.find_iter(ac_dir, "*.ac.v"):
            ac_ext0, ac_ext1 = os.path.splitext(ac_file)
            ac_tar_file = f"{os.path.splitext(ac_ext0)[0]}{ac_ext1}"
            shutil.copyfile(ac_file, ac_tar_file)
            subprocess.run(
                f"emacs --batch {ac_tar_file} -f verilog-auto -f save-buffer", shell=True)
            LOG.info("emacs auto connection generated file %s done", ac_tar_file)
    else:
        raise Exception("missing main arguments")
