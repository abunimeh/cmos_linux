"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj fm sub cmd entrence
"""

import os
import shutil
import subprocess
import datetime as dt
import requests
import pcom
import env_booter
import filelst_gen

LOG = pcom.gen_logger(__name__)

def proc_fm(ced, fm_cfg_dic):
    """to process and kick off fm flow"""
    ref_name = (
        fm_cfg_dic["fm"]["REF_NAME"] if fm_cfg_dic["fm"]["REF_NAME"]
        else fm_cfg_dic["fm"]["DESIGN_NAME"])
    imp_name = (
        fm_cfg_dic["fm"]["IMP_NAME"] if fm_cfg_dic["fm"]["IMP_NAME"]
        else fm_cfg_dic["fm"]["DESIGN_NAME"])
    fm_cfg_dic["fm"]["fm_time_dir"] = fm_time_dir = (
        f"{fm_cfg_dic['fm']['fm_top_dir']}{os.sep}fm_"
        f"{os.path.basename(fm_cfg_dic['fm']['fm_src_dir'])}_{imp_name}_{ref_name}_"
        f"{ced['TIME'].strftime('%Y_%m_%d_%H_%M_%S')}")
    os.makedirs(fm_time_dir, exist_ok=True)
    LOG.info("generate fm.tcl file")
    pcom.ren_tempfile(
        f"{fm_cfg_dic['fm']['fm_src_dir']}{os.sep}fm_template{os.sep}fm.tcl",
        f"{fm_time_dir}{os.sep}fm.tcl", fm_cfg_dic["fm"])
    fm_str = (
        f"cd {fm_time_dir} && fm_shell -f {fm_time_dir}{os.sep}fm.tcl "
        f"| tee -i {fm_time_dir}{os.sep}fm.log")
    subprocess.run(fm_str, shell=True)
    parse_rlt_dic = {
        "design_name": pcom.rd_cfg(fm_cfg_dic, "fm", "DESIGN_NAME", True),
        "proj": ced["PROJ_NAME"],
        "user": ced["USER_NAME"],
        "run_time": dt.datetime.timestamp(ced["TIME"]),
        "status": "passed" if os.path.isfile(f"{fm_time_dir}{os.sep}passed") else "failed"}
    query_url = "http://172.51.13.205:8000/pj_app/fm/db_query/query_insert_case/"
    requests.post(query_url, json=parse_rlt_dic)

def gen_fmfile(fm_file):
    """to generate fm ref and tar file"""
    if ".v" in fm_file:
        netlist_flag = True if "syn.v" in fm_file else False
        files = fm_file
    else:
        fm_tup = filelst_gen.FilelstGen().gen_file_lst([fm_file])
        _, verilog_lst, vhdl_lst = fm_tup
        files = os.linesep.join(verilog_lst+vhdl_lst)
        netlist_flag = True if "syn.v" in files else False
    return netlist_flag, files

def run_fm(args):
    """to run fm sub cmd"""
    if args.fm_ref_file and args.fm_imp_file:
        if not shutil.which("fm_shell"):
            raise Exception("fm is not loaded")
        ced, _ = env_booter.EnvBooter().boot_env()
        fm_src_dir = (
            os.path.abspath(os.path.expandvars(args.fm_src))
            if args.fm_src else f"{ced['FLOW_FM']}{os.sep}src")
        fm_cfg_dic = pcom.gen_cfg([f"{fm_src_dir}{os.sep}fm.cfg"])
        LOG.info("gegerating ref related file and flag")
        ref_netlist_flag, ref_files = gen_fmfile(args.fm_ref_file)
        fm_cfg_dic["fm"]["ref_netlist_flag"] = str(ref_netlist_flag)
        fm_cfg_dic["fm"]["ref_filelist"] = ref_files
        LOG.info("gegerating imp related file and flag")
        imp_netlist_flag, imp_files = gen_fmfile(args.fm_imp_file)
        fm_cfg_dic["fm"]["imp_netlist_flag"] = str(imp_netlist_flag)
        fm_cfg_dic["fm"]["imp_filelist"] = imp_files
        fm_cfg_dic["fm"]["fm_top_dir"] = ced["FLOW_FM"]
        fm_cfg_dic["fm"]["fm_src_dir"] = fm_src_dir
        proc_fm(ced, fm_cfg_dic)
    else:
        raise Exception("missing main arguments")
