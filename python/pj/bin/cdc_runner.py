"""
Author: Junxiu Liu @ CPU Verification Platform Group
Email: liujx@cpu.com.cn
Description: pj cdc sub cmd entrence
"""

import os
import re
import shutil
import subprocess
import pcom
import env_booter
import filelst_gen

LOG = pcom.gen_logger(__name__)

def run_compiler(cdct_dir, cdc_flist, err_pat):
    """to compile the rtl files"""
    for flist in cdc_flist:
        if not os.path.isfile(flist):
            raise Exception(f"base flist file {flist} is NA")
    dir_lst, verilog_lst, _ = filelst_gen.FilelstGen().gen_file_lst(cdc_flist)
    rtl_flist = f"{cdct_dir}{os.sep}rtl.flist"
    with open(rtl_flist, "w") as cff:
        cff.write(os.linesep.join(dir_lst+verilog_lst))
    log_file = f"{cdct_dir}{os.sep}compilation.log"
    compiler_str = (
        f"cd {cdct_dir} && vlog -f {rtl_flist} -l {log_file}")
    subprocess.run(compiler_str, shell=True)
    if os.path.isfile(log_file):
        with open(log_file) as lff:
            if err_pat.search(lff.read()):
                open(f"{cdct_dir}{os.sep}failed", "w").close()
                raise Exception(f"Error generated during run compilation")
def gen_post_wv(wv_dtl_rpt, cfg_dic):
    """to generate the post_waiver_rpt"""
    type_lst = []
    sp_ep_lst = []
    for sect in cfg_dic.sections():
        type_lst.extend(pcom.rd_cfg(cfg_dic, sect, "type"))
        sp_ep_lst.extend(pcom.rd_cfg(cfg_dic, sect, "sp|ep"))
    with open(wv_dtl_rpt) as drf:
        mop = pcom.REOpter(drf.read())
    str_pat = re.compile(
        rf"Violations{os.linesep}=+{os.linesep}(.*?){os.linesep}{{3,4}}", re.DOTALL)
    wv_lst = mop.group(1).split(f"{os.linesep*2}") if mop.search(str_pat) else []
    wv_pat = re.compile(rf"{os.linesep}-+{os.linesep}(.*)", re.DOTALL)
    result_lst = []
    for waiver in wv_lst:
        sop = pcom.REOpter(waiver)
        if sop.search(wv_pat):
            waiver = sop.group(1)
        if type_lst and re.search(
                "|".join([re.escape(cc).replace(r"\*", ".*") for cc in type_lst]), waiver):
            continue
        for sp_ep in sp_ep_lst:
            if "|" not in sp_ep:
                LOG.warning(f"the format of {sp_ep} is wrong")
                continue
            if re.search(
                    re.escape(sp_ep.split("|")[0]).replace(r"\*", ".*"),
                    waiver.split(os.linesep)[0]) and re.search(
                        re.escape(sp_ep.split("|")[1]).replace(r"\*", ".*"),
                        waiver.split(os.linesep)[1]):
                break
        else:
            result_lst.append(waiver)
    return result_lst
def proc_cdc(cdc_src):
    """to process cdc flow"""
    if not shutil.which("vlog"):
        raise Exception("qsim is not loaded")
    if not shutil.which("qverify"):
        raise Exception("formal is not loaded")
    ced, _ = env_booter.EnvBooter().boot_env()
    cdc_src_dir = (
        os.path.abspath(os.path.expandvars(cdc_src))
        if cdc_src else f"{ced['FLOW_CDC']}{os.sep}src")
    cdc_cfg_dic = pcom.gen_cfg([f"{cdc_src_dir}{os.sep}cdc.cfg"])
    wv_cfg_dic = pcom.gen_cfg([f"{cdc_src_dir}{os.sep}waiver.cfg"])
    cdc_flist = pcom.rd_cfg(cdc_cfg_dic, "cdc", "design_flist")
    top = pcom.rd_cfg(cdc_cfg_dic, "cdc", "design_top")
    if not cdc_flist or not top:
        raise Exception(f"no cdc filelist or top name found in cfg")
    cdc_time_dir = (
        f"{ced['FLOW_CDC']}{os.sep}cdc_{os.path.basename(cdc_src_dir)}_"
        f"{top[0]}_{ced['TIME'].strftime('%Y_%m_%d_%H_%M_%S')}")
    os.makedirs(cdc_time_dir, exist_ok=True)
    pcom.ren_tempfile(
        f"{cdc_src_dir}{os.sep}template{os.sep}cdc.tcl",
        f"{cdc_time_dir}{os.sep}cdc.tcl", cdc_cfg_dic["cdc"])
    compiler_err_pat = re.compile(
        "|".join([re.escape(cc) for cc in pcom.rd_cfg(cdc_cfg_dic, "cdc", "err_str")]))
    run_compiler(cdc_time_dir, cdc_flist, compiler_err_pat)
    if not os.path.isfile(f"{cdc_time_dir}{os.sep}failed"):
        cdc_str = (
            f"cd {cdc_time_dir} && "
            f"qverify -c -do {cdc_time_dir}{os.sep}cdc.tcl "
            f"-od {cdc_time_dir}{os.sep}Output_Results")
        subprocess.run(cdc_str, shell=True)
    dtl_rpt = f"{cdc_time_dir}{os.sep}Output_Results{os.sep}cdc_detail.rpt"
    if not os.path.isfile(dtl_rpt):
        raise Exception(f"report file {dtl_rpt} is not existed")
    result_lst = gen_post_wv(dtl_rpt, wv_cfg_dic)
    if result_lst:
        with open(f"{cdc_time_dir}{os.sep}post_waiver.rpt", "w") as pwr:
            for wv_rule in result_lst:
                pwr.write(wv_rule+os.linesep)
        LOG.warning("post waived violations exists, please check post_waiver.rpt file")
def run_cdc(args):
    """to run cdc sub cmd"""
    proc_cdc(args.cdc_src)
