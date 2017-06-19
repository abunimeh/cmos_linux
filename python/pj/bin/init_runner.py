"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj init sub cmd entrence
"""

import os
import getpass
import svn.remote
import svn.common
import pcom

LOG = pcom.gen_logger(__name__)

def check_out_dir(repo_base, dir_name, u_n, p_w):
    """to check out particular dir"""
    repo_dir = f"{repo_base}{dir_name}"
    cur_dir = f"{os.getcwd()}{os.sep}{dir_name}"
    LOG.info("checking out dir %s", repo_dir)
    repo = svn.remote.RemoteClient(
        repo_dir, username=u_n, password=p_w) if u_n and p_w else svn.remote.RemoteClient(repo_dir)
    repo.checkout(cur_dir)

def run_init(args):
    """to run init sub cmd"""
    if args.proj_name:
        repo_base = f"http://svn1/proj/{args.proj_name}/trunk/"
        try:
            repo = svn.remote.RemoteClient(repo_base)
            repo.info()
            u_n = ""
            p_w = ""
        except svn.common.SvnException:
            u_n = getpass.getuser()
            p_w = getpass.getpass("svn password: ")
        if args.sub_dir:
            check_out_dir(repo_base, "share", u_n, p_w)
            for s_d in args.sub_dir:
                check_out_dir(repo_base, s_d, u_n, p_w)
            open(f"{os.getcwd()}{os.sep}{pcom.FLAG_FILE}", "w").close()
        else:
            check_out_dir(repo_base, "", u_n, p_w)
    else:
        raise Exception("missing main arguments")
