"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: FPGASignalsGen class for FPGA dumping signlas generation
"""

import os
import re
import collections
import pcom

class FPGASignalsGen(object):
    """signal generator for FPGA signal file"""
    def __init__(self, ced):
        self.ced = ced
        self.h_dic = collections.defaultdict(list)
    def gen_h_lst(self):
        """to generate handle signal list"""
        for sv_file in pcom.find_iter(self.ced["MODULE_TB"], "*.sv"):
            with open(sv_file) as svf:
                for line in svf:
                    line = line.strip()
                    if line.startswith("$fwrite") and "handle0" in line and "%b" in line:
                        self.h_dic["h0"].append(re.search(r",(\w+)\s*\)\s*;", line).group(1))
                    elif line.startswith("$fwrite") and "handle1" in line and "%b" in line:
                        self.h_dic["h1"].append(re.search(r",(\w+)\s*\)\s*;", line).group(1))
    def gen_fpga_signals(self, cvsr_tup):
        """top execution function"""
        case, simv, seed, _ = cvsr_tup
        fs_file = os.path.join(self.ced["MODULE_OUTPUT"], case, f"{simv}__{seed}", "fpga_signals")
        h0_str = f"{os.linesep}    ".join(self.h_dic["h0"])
        h1_str = f"{os.linesep}    ".join(self.h_dic["h1"])
        fs_str = (
            f"handle0 (input):{os.linesep}    {h0_str}{os.linesep*2}"
            f"handle1 (output):{os.linesep}    {h1_str}")
        with open(fs_file, "w") as fsf:
            fsf.write(fs_str)
