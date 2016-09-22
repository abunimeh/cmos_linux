#! /usr/bin/env python3
### used to remove duplicated port mapping lines, leaving lower hierarchy port line

import argparse
import os
import collections
import re

def gen_args_top():
    parser = argparse.ArgumentParser()
    h_str = ("input signal file")
    parser.add_argument('-sf', dest='signal_file', required=True, help=h_str)
    h_str = ("input duplicated port signal file")
    parser.add_argument('-df', dest='dup_file', required=True, help=h_str)
    return parser.parse_args()

args = gen_args_top()
if not os.path.isfile(args.signal_file):
    os.sys.exit("signal file {0} is NA".format(args.signal_file))
if not os.path.isfile(args.dup_file):
    os.sys.exit("duplicated port signal file {0} is NA".format(args.dup_file))

sig_dic = collections.OrderedDict()
with open(args.signal_file) as sf:
    for line in sf:
        line = line.strip()
        if not line:
            continue
        item_lst = [cc.strip() for cc in line.split(',') if cc.strip()]
        if len(item_lst) != 6:
            os.sys.exit("file {0} line {1} has wrong format, which has {2} "
                        "items".format(args.signal_file, line, len(item_lst)))
        key_str = item_lst[2].replace('/', '.').strip('.')+'.'+item_lst[4]
        sig_dic[key_str] = line

with open(args.dup_file) as df:
    df_lst = re.split(r'^Count\(\d+\)$', df.read(), flags=re.M)

for df_pair in df_lst:
    df_pair = df_pair.strip()
    if not df_pair:
        continue
    df1, df2, *_ = df_pair.split(os.linesep)
    df1 = df1.strip()
    df2 = df2.strip()
    df = df1 if len(df1) < len(df2) else df2
    df_sig = re.sub(r'\[\d+:\d+\]', '', df)
    sig_dic.pop(df_sig, None)

signal_file_base, signal_file_ext = os.path.splitext(args.signal_file)
new_file = signal_file_base+'_new'+signal_file_ext
with open(new_file, 'w') as nf:
    for sig, line in sig_dic.items():
        nf.write(line+os.linesep)
