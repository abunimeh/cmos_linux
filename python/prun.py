#! /usr/bin/env python

##### modules
import pcom
import os
import re
import argparse
import fnmatch
import datetime as dt
import xlrd
import itertools
import shutil
import subprocess
import multiprocessing as mp
import multiprocessing.pool
import json
import pwd
import logging
import configparser
import random
import psycopg2
import csv
import bs4
import urllib.request

##### functions
def get_args_top():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    h_str = ("input log record file name <MUST come first>")
    parser.add_argument('-l', dest='log', help=h_str)

    h_str = ("sub cmd about kicking off regression")
    regr_parser = subparsers.add_parser('regr', help=h_str)
    h_str = ("input regression tracelist files to run")
    regr_parser.add_argument('-f', dest='regr_file', default=[], nargs='+',
                             help=h_str)
    regr_parser.set_defaults(func=main_regr)
    
    h_str = ("sub cmd about extracting files or urls")
    extract_parser = subparsers.add_parser('extract', help=h_str)
    group_fu = extract_parser.add_mutually_exclusive_group()
    h_str = ("input verilog file to extract module instance mapping")
    group_fu.add_argument('-f', dest='extract_file', default='', help=h_str)
    h_str = ("input url to extract regression table")
    group_fu.add_argument('-u', dest='extract_url', default='', help=h_str)
    h_str = ("input target file extracted <MUST follow -f|-u>")
    extract_parser.add_argument('-t', dest='extract_target',
                                default='extract_target', help=h_str)
    extract_parser.set_defaults(func=main_extract)

    return parser.parse_args()

def rd_cfg(sec, opt):
    return pcom.format_cfg_str(GED['CFG'].get(sec, opt, fallback=''))

def main_regr(args):
    if args.regr_file:
        pool = MyPool(50)
        ar = pool.map_async()
        pool.close()
        pool.join()
        ar.get()
        LOG.info("running regression files done")
    else:
        raise Exception("missing main arguments")

def main_extract(args):
    if args.extract_file:
        extract_file = os.path.abspath(os.path.expandvars(args.extract_file))
        if not os.path.isfile(extract_file):
            raise Exception("extract file {0} is NA".format(extract_file))
        with open(extract_file) as ef:
            comt_file = ef.read()
        sen_lst = re.sub(r'//.*|/\*(?:.|\n)*?\*/', '',
                         comt_file).expandtabs(1).split(';')
        target_dic = {}
        for sen_line in sen_lst:
            sen_line_st = sen_line.strip()
            if sen_line_st.startswith(('module ', 'input ', 'output ',
                                       'inout ', 'wire ', 'assign ')):
                continue
            ins_pat = re.match(r'(?:.*(?:end|`.*)\n\s*)?(\w+)\s+.*?'
                               '(u\d*_\w+\1)\s*\(.*', sen_line_st,
                               flags=re.DOTALL)
            if ins_pat:
                target_dic[ins_pat.group(2)] = inst_pat.group(1)
        with open(args.extract_target, 'w') as tf:
            for tar_key in sorted(target_dic):
                tf.write(tar_key+' '+target_dic[tar_key]+os.linesep)
        LOG.info("extracting RTL file done")
    elif args.extract_url:
        soup = bs4.BeautifulSoup(urllib.request.urlopen(args.extract_url),
                                 'html.parser')
        table = soup.find('table', attrs={'id': 'my_table'})
        headers = [header.text.replace(',', '&') for header in
                   table.find_all('th')]
        rows = []
        for row in table.find_all('tr'):
            rows.append([val.text.replace(',', '&') for val in
                         row.find_all('td')])
        with open(args.extract_target, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, quotechar='',
                                escapechar='"')
            writer.writerow(headers)
            writer.writerows(row for row in rows if row)
        LOG.info("extracting url {0} done".format(args.extract_url))
    else:
        raise Exception("missing main arguments")

##### classes

##### main
def main(main_flg=True):
    if main_flg:
        args = get_args_top()
    global LOG
    LOG = pcom.gen_logger(file_log=args.log) if main_flg else pcom.gen_logger(
        con_level=logging.WARNING)
    global GED
    GED = pcom.gen_env_dic(['USER', 'HOME'])
    GED['TIME'] = dt.datetime.now()
    com_cfg_file = GED['HOME']+os.sep+'com.cfg'
    if not os.path.isfile(com_cfg_file):
        LOG.warning("common config file{0} is NA".format(com_cfg_file))
    GED['CFG'] = pcom.gen_cfg([com_cfg_file])
    LOG.info("commence...")
    if main_flg:
        args.func(args)
    LOG.info("complete")

if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        LOG.exception(ex)
else:
     main(False)
