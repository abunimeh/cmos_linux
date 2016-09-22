# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: FPGASignalsGen class for FPGA dumping signlas generation

### modules
import pcom
import os
import re

### classes
class FPGASignalsGen(object):
    def __init__(self, ced):
        self.ced = ced
        self.h0_lst = []
        self.h1_lst = []
    def gen_h_lst(self):
        for sv_file in pcom.find_iter(self.ced['MODULE_TB'], '*.sv'):
            with open(sv_file) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(
                            '$fwrite') and 'handle0' in line and '%b' in line:
                        self.h0_lst.append(
                            re.search(r',(\w+)\s*\)\s*;', line).group(1))
                    elif line.startswith(
                            '$fwrite') and 'handle1' in line and '%b' in line:
                        self.h1_lst.append(
                            re.search(r',(\w+)\s*\)\s*;', line).group(1))
    def gen_fpga_signals(self, ngs_tup):
        name, group, seed = ngs_tup
        fs_file = os.path.join(
            self.ced['MODULE_OUTPUT'], name, seed, 'fpga_signals')
        with open(fs_file, 'w') as f:
            f.write('handle0 (input):'+os.linesep+'    ')
            f.write((os.linesep+'    ').join(self.h0_lst))
            f.write(os.linesep*2+'handle1 (output):'+os.linesep+'    ')
            f.write((os.linesep+'    ').join(self.h1_lst))
