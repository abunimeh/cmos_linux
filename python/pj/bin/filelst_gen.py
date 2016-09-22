# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: FilelstGen class for flist recursively generation

### modules
import pcom
import os
import collections
import re

### classes
class FilelstGen(object):
    def __init__(self, LOG=None):
        self.LOG = LOG if LOG else pcom.gen_logger()
        self.file_dic = collections.OrderedDict()
        self.dir_lst = []
        self.nwd_lst = []
    def cov_f2lst(self, f, nwd):
        self.nwd_lst.append(os.getcwd())
        os.chdir(nwd)
        with open(f) as ff:
            for line in ff:
                line = line.strip()
                if not line:
                    continue
                line = os.path.expandvars(line)
                if '//' in line or '#' in line:
                    line = re.sub(r'(//|#).*$', '', line).strip()
                    if not line:
                        continue
                if line.startswith('-f '):
                    new_line = os.path.abspath(line[3:].strip())
                    if not os.path.isfile(new_line):
                        raise Exception("file line {0} in flist {1} is NA"
                                        "".format(line, f))
                    self.cov_f2lst(new_line, os.path.dirname(new_line))
                elif line.startswith('+incdir+'):
                    new_line = os.path.abspath(line[8:].strip())
                    if not os.path.isdir(new_line):
                        raise Exception("dir line {0} in flist {1} is NA"
                                        "".format(line, f))
                    self.dir_lst.append('+incdir+'+new_line)
                elif line.startswith('+define+'):
                    self.file_dic[line+'__'+str(len(self.file_dic))] = line
                else:
                    new_line = os.path.abspath(line)
                    if not os.path.isfile(new_line):
                        raise Exception("file line {0} in flist {1} is NA"
                                        "".format(new_line, f))
                    file_name = os.path.basename(new_line)
                    if file_name in self.file_dic:
                        self.LOG.info("duplicated files {0} and {1}, taking "
                                      "first met file {1}".format(
                                          new_line, self.file_dic[file_name]))
                        continue
                    self.file_dic[file_name] = new_line
        os.chdir(self.nwd_lst.pop())
    def gen_file_lst(self, flist_lst):
        vlog_lst = []
        vhdl_lst = []
        for rf in flist_lst:
            rf = os.path.abspath(os.path.expandvars(rf.strip()))
            if not os.path.isfile(rf):
                raise Exception("file {0} is NA".format(rf))
            self.cov_f2lst(rf, os.path.dirname(rf))
        for file_name, file_line in self.file_dic.items():
            if file_line.endswith(('.vhdl', '.vhd')):
                vhdl_lst.append(file_line)
            else:
                vlog_lst.append(file_line)
        return (self.dir_lst, vlog_lst, vhdl_lst)
