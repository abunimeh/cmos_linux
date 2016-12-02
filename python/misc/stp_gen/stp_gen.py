#! /usr/bin/env python3
### used to generate stp from text files provided

import argparse
import os
import re
import collections
import datetime as dt
import jinja2

class REOpter(object):
    def __init__(self, re_str):
        self.re_str = re_str
    def match(self, re_rs):
        self.re_result = re.match(re_rs, self.re_str)
        return bool(self.re_result)
    def search(self, re_rs):
        self.re_result = re.search(re_rs, self.re_str)
        return bool(self.re_result)
    def group(self, i):
        return self.re_result.group(i)

def gen_args_top():
    parser = argparse.ArgumentParser()
    h_str = ("input signals text file")
    parser.add_argument('-txt', dest='txt_file', required=True, help=h_str)
    return parser.parse_args()

args = gen_args_top()

if not os.path.isfile(args.txt_file):
    os.sys.exit("signals text file {0} is NA".format(args.txt_file))

group_dic = collections.OrderedDict()
with open(args.txt_file) as tf:
    for line in tf:
        line = line.strip()
        m = REOpter(line)
        if m.match(r'signal:\s+([/\w]+)(?:\[(\d+):(\d+)\])?,\s+\w+:\s+(\d+),'):
            group_name = 'Group{0}'.format(m.group(4))
            if group_name not in group_dic:
                group_dic[group_name] = []
            sig_lst = m.group(1).split('/')
            new_sig_lst = []
            for index, part in enumerate(sig_lst):
                if index == len(sig_lst)-1:
                    new_sig_lst.append(part)
                elif part.startswith('u_'):
                    new_sig_lst.append('{0}:{1}'.format(part[2:], part))
                elif part.endswith('_inst'):
                    new_sig_lst.append('{0}:{1}'.format(part[:-5], part))
            new_sig = '|'.join(new_sig_lst)
            if m.group(2) and m.group(3):
                for i in range(int(m.group(3)), int(m.group(2))+1):
                    group_dic[group_name].append('{0}[{1}]'.format(new_sig, i))
            else:
                group_dic[group_name].append(new_sig)

inst_dic_lst = []
for index_org, group in enumerate(group_dic):
    offset = int(index_org/50)
    index = index_org%50
    if index == 0:
        inst_dic = {'inst_num': offset,
                    'inst_time': dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                    'group_dic': {}}
        inst_dic_lst.append(inst_dic)
    inst_dic['group_dic']['{0:04d}'.format(index_org)] = []
    for index_sig, signal in enumerate(reversed(group_dic[group])):
        inst_dic['group_dic']['{0:04d}'.format(index_org)].append({'index': index_sig, 'sig_name': signal})

dir_name = os.path.dirname(os.path.realpath(__file__))
templateLoader = jinja2.FileSystemLoader(dir_name)
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('template.stp')
template_out = template.render({'inst_dic_lst': inst_dic_lst})

stp_file = os.path.splitext(args.txt_file)[0]+'.stp'
with open(stp_file, 'w') as f:
    f.write(template_out)
