"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj init sub cmd entrence
"""

import os
import getpass
import svn.remote
import svn.exception
import requests
import pcom

LOG = pcom.gen_logger(__name__)

def check_out_dir(repo_base, dir_name, u_n, p_w):
    """to check out particular dir"""
    repo_dir = f"{repo_base}{os.sep}{dir_name}"
    cur_dir = f"{os.getcwd()}{os.sep}{dir_name}"
    LOG.info("checking out dir %s", repo_dir)
    repo = svn.remote.RemoteClient(
        repo_dir, username=u_n, password=p_w) if u_n and p_w else svn.remote.RemoteClient(repo_dir)
    if dir_name.endswith(pcom.FLAG_FILE):
        repo.export(cur_dir)
    else:
        repo.checkout(cur_dir)

def np_check_out(sub_dir_lst, repo_base, u_n, p_w):
    """to process normal project checking out dir actions"""
    if sub_dir_lst:
        check_out_dir(repo_base, "share", u_n, p_w)
        for s_d in sub_dir_lst:
            check_out_dir(repo_base, s_d, u_n, p_w)
        if not repo_base.endswith("tools"):
            open(f"{os.getcwd()}{os.sep}{pcom.FLAG_FILE}", "w").close()
    else:
        check_out_dir(repo_base, "", u_n, p_w)

def sp_check_out(proj_name, sub_dir_lst, repo_base, u_n, p_w):
    """to process svn project checking out dir actions"""
    dir_query_url = (
        f"http://172.51.13.205:8000/user_info/svn/query_dir_lst/?user={u_n}&proj={proj_name}")
    avail_dir_lst = requests.get(dir_query_url).json()
    if sub_dir_lst:
        check_out_dir(repo_base, "share", u_n, p_w)
        for s_d in sub_dir_lst:
            for avail_dir in avail_dir_lst:
                if s_d not in avail_dir:
                    continue
                check_out_dir(repo_base, avail_dir, u_n, p_w)
        if not repo_base.endswith("tools"):
            open(f"{os.getcwd()}{os.sep}{pcom.FLAG_FILE}", "w").close()
    else:
        for avail_dir in avail_dir_lst:
            check_out_dir(repo_base, avail_dir, u_n, p_w)

def run_init(args):
    """to run init sub cmd"""
    normal_proj_dic = {"cpu0": "http://svn1/proj/cpu0/trunk",
                       "cpu1_pre": "http://svn1/proj/cpu1_pre/trunk",
                       "cpu1_proto": "http://svn1/proj/cpu1_proto",
                       "tools": "http://svn1/tools/tools"}
    svn_proj_dic = {"cpu1": "http://svn1/proj/cpu1"}
    all_proj_dic = {}
    all_proj_dic.update(normal_proj_dic)
    all_proj_dic.update(svn_proj_dic)
    if args.proj_list:
        proj_lst = sorted(list(all_proj_dic))
        str_lst = [f"{os.linesep}all available projects"]
        str_lst.append("*"*30)
        str_lst.extend(proj_lst)
        str_lst.append("*"*30)
        LOG.info(os.linesep.join(str_lst))
        return
    elif args.proj_name:
        if args.proj_name not in all_proj_dic:
            raise Exception(f"proj name must be one of {proj_lst}")
        repo_base = all_proj_dic[args.proj_name]
        try:
            repo = svn.remote.RemoteClient(repo_base)
            repo.info()
            u_n = ""
            p_w = ""
        except svn.exception.SvnException:
            u_n = getpass.getuser()
            p_w = getpass.getpass("svn password: ")
        if args.proj_name in normal_proj_dic:
            np_check_out(args.sub_dir, repo_base, u_n, p_w)
        else:
            sp_check_out(args.proj_name, args.sub_dir, repo_base, u_n, p_w)
    else:
        raise Exception("missing main arguments")
