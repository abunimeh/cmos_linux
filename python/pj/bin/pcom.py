# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: fundamental functions and classes

##### modules
import os
import re
import fnmatch
import multiprocessing as mp
import multiprocessing.pool
import logging
import configparser
import psutil

##### functions
def gen_logger(con_level=logging.INFO, file_log=False):
    logger = logging.getLogger('cmos_py')
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(con_level)
    formatter = ColoredFormatter('{asctime} {levelname} {message}', '%H:%M:%S',
                                 style='{')
    console.setFormatter(formatter)
    logger.addHandler(console)
    if file_log:
        file_log = logging.FileHandler(file_log, 'w')
        file_log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('{asctime} {name} {funcName} {lineno} '
                                      '[{levelname}] {message}', style='{')
        file_log.setFormatter(formatter)
        logger.addHandler(file_log)
    return logger

def gen_cfg(cfg_file_iter, d=('=', ':')):
    config = configparser.ConfigParser(allow_no_value=True, delimiters=d)
    config.optionxform = str
    config.SECTCRE = re.compile(r'\[\s*(?P<header>[^]]+?)\s*\]')
    for cfg_file in cfg_file_iter:
        config.read(cfg_file)
    return config

def rd_cfg(cfg, sec, opt):
    value_str = os.path.expandvars(cfg.get(sec, opt, fallback=''))
    if not value_str:
        value_str = ''
    split_str = r'{0}'.format(os.linesep) if opt.endswith(
        '_opts') else r',|{0}'.format(os.linesep)
    return [cc.strip() for cc in re.split(split_str, value_str) if cc]

def find_iter(path, pattern, dir_flg=False, cur_flg=False, i_str=''):
    if cur_flg:
        find_lst = os.listdir(path)
        for find_name in fnmatch.filter(find_lst, pattern):
            if i_str and i_str in find_name:
                continue
            root_find_name = os.path.join(path, find_name)
            if os.access(root_find_name, os.R_OK):
                if dir_flg and os.path.isdir(root_find_name):
                    yield root_find_name
                elif not dir_flg and os.path.isfile(root_find_name):
                    yield root_find_name
    else:
        for root_name, dir_name_lst, file_name_lst in os.walk(
                path, followlinks=False):
            find_lst = dir_name_lst if dir_flg else file_name_lst
            for find_name in fnmatch.filter(find_lst, pattern):
                if i_str and i_str in find_name:
                    continue
                root_find_name = os.path.join(root_name, find_name)
                if os.access(root_find_name, os.R_OK):
                    yield root_find_name

def pterminate(proc_pid):
    proc = psutil.Process(proc_pid)
    for sub_proc in proc.children(recursive=True):
        sub_proc.terminate()
    proc.terminate()

def pkill(proc_pid):
    proc = psutil.Process(proc_pid)
    for sub_proc in proc.children(recursive=True):
        sub_proc.kill()
    proc.kill()

##### classes
class NoDaemonProcess(mp.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class MyPool(mp.pool.Pool):
    Process = NoDaemonProcess

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        LOG_COLORS = {'DEBUG': '\033[1;35m[DEBUG]\033[1;0m',
                      'INFO': '\033[1;34m[INFO]\033[1;0m',
                      'WARNING': '\033[1;33m[WARNING]\033[1;0m',
                      'ERROR': '\033[1;31m[ERROR]\033[1;0m',
                      'CRITICAL': '\033[1;31m[CRITICAL]\033[1;0m'}
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
        return msg.replace(level_name, LOG_COLORS.get(level_name, level_name))

class REOpter(object):
    def __init__(self, re_str):
        self.re_str = re_str
    def match(self, re_pat):
        self.re_result = re_pat.match(self.re_str)
        return bool(self.re_result)
    def search(self, re_pat):
        self.re_result = re_pat.search(self.re_str)
        return bool(self.re_result)
    def group(self, i):
        return self.re_result.group(i)
