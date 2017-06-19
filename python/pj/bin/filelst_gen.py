"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: FilelstGen class for flist recursively generation
"""

import os
import re
import collections
import pcom

LOG = pcom.gen_logger(__name__)

class FilelstGen(object):
    """recursive file list generator for eda simulation tools"""
    def __init__(self):
        self.file_dic = collections.OrderedDict()
        self.dir_lst = []
        self.nwd_lst = []
    def cov_file2lst(self, ffile, nwd):
        """recursive filelist expansion function"""
        self.nwd_lst.append(os.getcwd())
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
                    self.cov_file2lst(new_line, os.path.dirname(new_line))
                elif line.startswith("+incdir+"):
                    new_line = os.path.abspath(line[8:].strip())
                    if not os.path.isdir(new_line):
                        raise Exception(f"dir line {line} in flist {fff} is NA")
                    self.dir_lst.append(f"+incdir+{new_line}")
                elif line.startswith("+define+"):
                    self.file_dic[f"{line}__{len(self.file_dic)}"] = line
                else:
                    new_line = os.path.abspath(line)
                    if not os.path.isfile(new_line):
                        raise Exception(f"file line {new_line} in flist {fff} is NA")
                    file_name = os.path.basename(new_line)
                    if file_name in self.file_dic:
                        LOG.info(
                            "duplicated files %s and %s, taking the former "
                            "which is the first met one", self.file_dic[file_name], new_line)
                        continue
                    self.file_dic[file_name] = new_line
        os.chdir(self.nwd_lst.pop())
    def gen_file_lst(self, flist_lst):
        """top execution function"""
        vlog_lst = []
        vhdl_lst = []
        for flist in flist_lst:
            flist = os.path.abspath(os.path.expandvars(flist.strip()))
            if not os.path.isfile(flist):
                raise Exception(f"file {flist} is NA")
            self.cov_file2lst(flist, os.path.dirname(flist))
        for _, file_line in self.file_dic.items():
            if file_line.endswith((".vhdl", ".vhd")):
                vhdl_lst.append(file_line)
            else:
                vlog_lst.append(file_line)
        return self.dir_lst, vlog_lst, vhdl_lst
