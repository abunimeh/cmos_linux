"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: MakefileGen class for sim/regr simv/case makefile generation
"""

import os
import random
import json
import pickle
import collections
import pcom
import env_booter
import filelst_gen

LOG = pcom.gen_logger(__name__)

def check_seed(seed, seed_set):
    """to check seed in seed set recursively"""
    if seed in seed_set:
        return check_seed(seed+1, seed_set)
    return seed

class MakefileGen(object):
    """simulation flow makefiles generator for pj"""
    def __init__(self, ced, cfg_dic, mkg_dic):
        self.ced = ced
        self.cfg_dic = cfg_dic
        self.mkg_dic = mkg_dic
        c_src = f"{ced['MODULE_C']}{os.sep}src"
        self.mkg_dic["clib_flg"] = True if os.path.isdir(ced["MODULE_C"]) and (
            list(pcom.find_iter(ced["MODULE_C"], "*.c"))
            or list(pcom.find_iter(ced["MODULE_C"], "*.cpp"))
            or list(pcom.find_iter(ced["MODULE_C"], "*.cc"))
            or list(pcom.find_iter(ced["MODULE_C"], "*.cxx"))) else False
        self.mkg_dic["csrc_flg"] = True if os.path.isdir(c_src) and (
            list(pcom.find_iter(c_src, "*.c"))
            or list(pcom.find_iter(c_src, "*.cpp"))
            or list(pcom.find_iter(c_src, "*.cc"))
            or list(pcom.find_iter(c_src, "*.cxx"))) else False
        self.simv_set = {"DEFAULT"}
    def chk_c_cfg(self):
        """to check c options modification"""
        c_cfg_json = f"{self.ced['OUTPUT_CLIB']}{os.sep}c_cfg.json"
        os.makedirs(self.ced["OUTPUT_CLIB"], exist_ok=True)
        ojson = {}
        if os.path.isfile(c_cfg_json):
            with open(c_cfg_json) as cjf:
                ojson = json.load(cjf)
        njson = dict(self.cfg_dic["c"]["DEFAULT"])
        if ojson != njson or ojson == njson == {} or self.mkg_dic["fresh_flg"]:
            with open(c_cfg_json, "w") as cjf:
                json.dump(njson, cjf)
    def chk_simv_cfg(self, v_n):
        """to check simv options modification"""
        vn_cfg = self.cfg_dic["simv"][v_n]
        vg_dir = f"{self.ced['OUTPUT_SIMV']}{os.sep}{v_n}"
        simv_cfg_json = f"{vg_dir}{os.sep}simv_cfg.json"
        os.makedirs(vg_dir, exist_ok=True)
        ojson = {}
        if os.path.isfile(simv_cfg_json):
            with open(simv_cfg_json) as sjf:
                ojson = json.load(sjf)
        self.cfg_dic["simv"]["DEFAULT"].update(vn_cfg)
        njson = dict(self.cfg_dic["simv"]["DEFAULT"])
        if ojson != njson or ojson == njson == {} or self.mkg_dic["fresh_flg"]:
            with open(simv_cfg_json, "w") as sjf:
                json.dump(njson, sjf)
    def gen_smf_lst(self, v_n):
        """to generate sub modules filelist list"""
        smf_lst = []
        for s_m in pcom.rd_cfg(self.cfg_dic["simv"], v_n, "sub_modules"):
            if not ":" in s_m:
                raise Exception(
                    f"sub_modules {s_m} in module {self.ced['MODULE']} simv cfg "
                    f"has incorrect name:type format")
            m_name, m_type, *_ = s_m.split(":")
            module_dir = env_booter.find_module_dir(self.ced, self.cfg_dic, m_name)
            sm_flist = os.sep.join([module_dir, "flist", f"{m_type}.flist"])
            if not os.path.isfile(sm_flist):
                raise Exception(f"sub_modules {s_m} has no such file {sm_flist}")
            smf_lst.append(sm_flist)
        return smf_lst
    def chk_simv_flist(self, v_n, f_tup, tb_flg=False):
        """to check simv expanded filelist"""
        gf_dir = f"{self.ced['OUTPUT_SIMV']}{os.sep}{v_n}"
        fn_str = "simv_tbfl.pcl" if tb_flg else "simv_dutfl.pcl"
        simv_flist_pcl = f"{gf_dir}{os.sep}{fn_str}"
        os.makedirs(gf_dir, exist_ok=True)
        opcl = ()
        if os.path.isfile(simv_flist_pcl):
            with open(simv_flist_pcl, "rb") as spf:
                opcl = pickle.load(spf)
        npcl = f_tup
        if opcl != npcl:
            with open(simv_flist_pcl, "wb") as spf:
                pickle.dump(npcl, spf)
    def gen_cda_opts(self, v_n):
        """to generate customized dut analysis opts"""
        cda_opts_lst = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "custom_dut_ana_opts")
        if self.mkg_dic["regr_flg"]:
            cda_opts_lst = pcom.rd_cfg(
                self.cfg_dic["proj"], "regression_opts", "custom_dut_ana_opts")+cda_opts_lst
        fpga_cda_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "fpga_dut_ana_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "fpga") == ["on"] else []
        uvm_cda_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "uvm_dut_ana_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "uvm") == ["on"] else []
        upf_cda_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "upf_dut_ana_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "upf") == ["on"] else []
        return " ".join(cda_opts_lst+fpga_cda_lst+uvm_cda_lst+upf_cda_lst)
    def gen_cta_opts(self, v_n):
        """to generate customized tb analysis opts"""
        cta_opts_lst = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "custom_tb_ana_opts")
        if self.mkg_dic["regr_flg"]:
            cta_opts_lst = pcom.rd_cfg(
                self.cfg_dic["proj"], "regression_opts", "custom_tb_ana_opts")+cta_opts_lst
        fpga_cta_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "fpga_tb_ana_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "fpga") == ["on"] else []
        uvm_cta_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "uvm_tb_ana_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "uvm") == ["on"] else []
        upf_cta_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "upf_tb_ana_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "upf") == ["on"] else []
        return " ".join(cta_opts_lst+fpga_cta_lst+uvm_cta_lst+upf_cta_lst)
    def gen_ce_opts(self, v_n, simv_dic):
        """to generate customized elaboration opts"""
        ce_opts_lst = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "custom_elab_opts")
        if self.mkg_dic["regr_flg"]:
            ce_opts_lst = pcom.rd_cfg(
                self.cfg_dic["proj"], "regression_opts", "custom_elab_opts")+ce_opts_lst
        cov_ce_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "cov_elab_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "cov") == ["on"] else []
        wave_ce_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "wave_elab_opts")+pcom.rd_cfg(
                self.cfg_dic["simv"], v_n,
                f"wf_{simv_dic['wave_format']}_elab_opts") if pcom.rd_cfg(
                    self.cfg_dic["simv"], v_n, "wave") == ["on"] else []
        gui_ce_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "gui_elab_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "gui") == ["on"] else []
        prof_ce_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "prof_elab_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "prof") == ["on"] else []
        uvm_ce_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "uvm_elab_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "uvm") == ["on"] else []
        upf_ce_lst = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "upf_elab_opts") if pcom.rd_cfg(
                self.cfg_dic["simv"], v_n, "upf") == ["on"] else []
        return " ".join(
            ce_opts_lst+cov_ce_lst+wave_ce_lst+gui_ce_lst+prof_ce_lst+uvm_ce_lst+upf_ce_lst)
    def gen_simv_dic(self, v_n):
        """to generate simv related dic to render jinja2"""
        self.chk_simv_cfg(v_n)
        simv_dic = {"name": v_n}
        simv_dic["wave_format"] = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "wave_format", True, "fsdb")
        simv_dic["cda_opts"] = self.gen_cda_opts(v_n)
        simv_dic["cta_opts"] = self.gen_cta_opts(v_n)
        simv_dic["ce_opts"] = self.gen_ce_opts(v_n, simv_dic)
        simv_dic["upf_flg"] = True if pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "upf") == ["on"] else False
        dut_flist_lst = [f"{self.ced['MODULE_FLIST']}{os.sep}rtl.flist"]+self.gen_smf_lst(v_n)
        df_tup = filelst_gen.FilelstGen().gen_file_lst(dut_flist_lst)
        simv_dic["dut_dir_lst"], simv_dic["dut_file_lst"], simv_dic["vhdl_file_lst"] = df_tup
        self.chk_simv_flist(v_n, df_tup, False)
        tb_flist_lst = [f"{self.ced['MODULE_FLIST']}{os.sep}tb.flist"]
        tf_tup = filelst_gen.FilelstGen().gen_file_lst(tb_flist_lst)
        simv_dic["tb_dir_lst"], simv_dic["tb_file_lst"], _ = tf_tup
        self.chk_simv_flist(v_n, tf_tup, True)
        simv_dic["tb_dep_file_lst"] = list(
            pcom.find_iter(f"{self.ced['PROJ_VERIF']}{os.sep}vip", "*.sv"))+list(
                pcom.find_iter(self.ced["MODULE_TB"], "*.sv*"))
        simv_dic["vhdl_tool"] = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "vhdl_tool", True, "vhdlan")
        simv_dic["vhdl_da_opts"] = " ".join(pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, f"vt_{simv_dic['vhdl_tool']}_dut_ana_opts"))
        simv_dic["vhdl_ta_opts"] = " ".join(pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, f"vt_{simv_dic['vhdl_tool']}_tb_ana_opts"))
        simv_dic["ana_tool"] = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "ana_tool", True, "vlogan")
        simv_dic["da_opts"] = " ".join(pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, f"at_{simv_dic['ana_tool']}_dut_ana_opts"))
        simv_dic["ta_opts"] = " ".join(pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, f"at_{simv_dic['ana_tool']}_tb_ana_opts"))
        simv_dic["elab_tool"] = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "elab_tool", True, "vcs")
        simv_dic["e_opts"] = " ".join(pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, f"et_{simv_dic['elab_tool']}_elab_opts"))
        simv_dic["w_opts"] = " ".join(pcom.rd_cfg(self.cfg_dic["simv"], v_n, "verdi_opts"))
        simv_dic["tb_top"] = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "tb_top", True, "test_top")
        simv_dic["power_top"] = pcom.rd_cfg(
            self.cfg_dic["simv"], v_n, "power_top", True, "chip_top")
        simv_dic["pre_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "pre_cmd")
        simv_dic["post_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["simv"], v_n, "post_cmd")
        simv_dic["file_dic"] = {}
        for opt_name, opt_cont in self.cfg_dic["simv"][v_n].items():
            if not opt_name.startswith("file__"):
                continue
            simv_dic["file_dic"][opt_name[6:]] = opt_cont.replace(
                "$", "$$").replace("\\", "").split(os.linesep)
        return simv_dic
    def gen_su_opts(self, c_n, case_dic):
        """to generate customized simulation opts"""
        su_opts_lst = pcom.rd_cfg(self.cfg_dic["case"], c_n, "custom_simu_opts")
        if self.mkg_dic["regr_flg"]:
            su_opts_lst = pcom.rd_cfg(
                self.cfg_dic["proj"], "regression_opts", "custom_simu_opts")+su_opts_lst
        cov_su_lst = pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "cov_simu_opts") if pcom.rd_cfg(
                self.cfg_dic["case"], c_n, "cov") == ["on"] else []
        wave_su_lst = pcom.rd_cfg(
            self.cfg_dic["case"], c_n,
            f"wf_{case_dic['wave_format']}_simu_opts") if pcom.rd_cfg(
                self.cfg_dic["case"], c_n, "wave") == ["on"] else []
        wg_su_lst = pcom.rd_cfg(
            self.cfg_dic["case"], c_n,
            f"wf_{case_dic['wave_format']}_glitch_simu_opts") if pcom.rd_cfg(
                self.cfg_dic["case"], c_n, "wave") == ["on"] and pcom.rd_cfg(
                    self.cfg_dic["case"], c_n, "wave_glitch") == ["on"] else []
        seed_su_lst = pcom.rd_cfg(self.cfg_dic["case"], c_n, "seed_simu_opts")
        uvm_su_lst = pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "uvm_simu_opts") if pcom.rd_cfg(
                self.cfg_dic["case"], c_n, "uvm") == ["on"] else []
        gui_su_lst = pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "gui_simu_opts") if pcom.rd_cfg(
                self.cfg_dic["case"], c_n, "gui") == ["on"] else []
        prof_mem_su_lst = pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "prof_mem_simu_opts") if pcom.rd_cfg(
                self.cfg_dic["case"], c_n, "prof_mem") == ["on"] else []
        prof_time_su_lst = pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "prof_time_simu_opts") if pcom.rd_cfg(
                self.cfg_dic["case"], c_n, "prof_time") == ["on"] else []
        return " ".join(
            su_opts_lst+cov_su_lst+wave_su_lst+wg_su_lst+seed_su_lst+uvm_su_lst+gui_su_lst+
            prof_mem_su_lst+prof_time_su_lst)
    def gen_case_dic(self, c_n):
        """to generate case related dic to render jinja2"""
        case_dic = {"name": c_n}
        simv_str = pcom.rd_cfg(self.cfg_dic["case"], c_n, "simv", True)
        case_dic["simv"] = simv_str if simv_str and simv_str in self.cfg_dic["simv"] else "DEFAULT"
        self.simv_set.add(case_dic["simv"])
        case_dic["tb_top"] = pcom.rd_cfg(
            self.cfg_dic["simv"], case_dic["simv"], "tb_top", True, "test_top")
        case_dic["wave"] = True if pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "wave") == ["on"] else False
        case_dic["wave_format"] = pcom.rd_cfg(
            self.cfg_dic["simv"], case_dic["simv"], "wave_format", True, "fsdb")
        case_dic["wave_mem"] = True if pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "wave_mem") == ["on"] else False
        case_dic["wave_glitch"] = True if pcom.rd_cfg(
            self.cfg_dic["case"], c_n, "wave_glitch") == ["on"] else False
        case_dic["su_opts"] = self.gen_su_opts(c_n, case_dic)
        case_dic["w_opts"] = " ".join(pcom.rd_cfg(
            self.cfg_dic["simv"], case_dic["simv"], "verdi_opts"))
        case_dic["pre_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["case"], c_n, "pre_cmd")
        case_dic["post_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["case"], c_n, "post_cmd")
        case_dic["file_dic"] = {}
        for opt_name, opt_cont in self.cfg_dic["case"][c_n].items():
            if not opt_name.startswith("file__"):
                continue
            case_dic["file_dic"][opt_name[6:]] = opt_cont.replace(
                "$", "$$").replace("\\", "").split(os.linesep)
        case_dic["regr_type_lst"] = pcom.rd_cfg(self.cfg_dic["case"], c_n, "regression_type")
        case_dic["regr_type_lst"].append("all")
        seed_set = set()
        seed_str = pcom.rd_cfg(self.cfg_dic["case"], c_n, "seed", True)
        rt_str = pcom.rd_cfg(self.cfg_dic["case"], c_n, "random_times", True)
        loop_times = rt_str if rt_str and rt_str.isdigit() else "1"
        for _ in range(int(loop_times)):
            if rt_str:
                seed = check_seed(random.randrange(1, 999999), seed_set)
                seed_set.add(seed)
            elif seed_str:
                if seed_str.isdigit():
                    seed_set.add(int(seed_str))
                else:
                    seed = check_seed(random.randrange(1, 999999), seed_set)
                    seed_set.add(seed)
            else:
                seed_set.add(1)
        case_dic["seed_set"] = seed_set
        return case_dic
    def gen_makefile(self):
        """to generate top makefile"""
        mk_dic = {"CED": self.ced}
        mk_dic["clib_flg"] = self.mkg_dic["clib_flg"]
        mk_dic["csrc_flg"] = self.mkg_dic["csrc_flg"]
        self.cfg_dic["c"]["DEFAULT"].update(self.mkg_dic["ow_dic"]["pre"])
        self.chk_c_cfg()
        mk_dic["base_comp_opts"] = " ".join(
            pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "base_comp_opts"))
        mk_dic["lib_comp_opts"] = " ".join(
            pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "lib_comp_opts"))
        mk_dic["src_comp_opts"] = " ".join(
            pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "src_comp_opts"))
        mk_dic["src_run_opts"] = " ".join(
            pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "src_run_opts"))
        mk_dic["lib_pre_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "lib_pre_cmd")
        mk_dic["lib_post_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "lib_post_cmd")
        mk_dic["src_pre_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "src_pre_cmd")
        mk_dic["src_post_cmd_lst"] = pcom.rd_cfg(self.cfg_dic["c"], "DEFAULT", "src_post_cmd")
        mk_dir = self.ced["MODULE_OUTPUT"]
        mk_file = "Makefile"
        os.makedirs(mk_dir, exist_ok=True)
        LOG.info("output dir %s is generated", mk_dir)
        pcom.ren_tempfile(
            f"{self.ced['PJ_TEMPLATES']}{os.sep}{mk_file}", f"{mk_dir}{os.sep}{mk_file}", mk_dic)
        return mk_dir, mk_file
    def gen_simv_makefile(self, simv_dic):
        """to generate simv makefile"""
        ms_dic = {"CED": self.ced, "simv_dic": simv_dic, "ed": {"simv": simv_dic["name"]}}
        ms_dic["clib_flg"] = self.mkg_dic["clib_flg"]
        ms_dir = f"{self.ced['OUTPUT_SIMV']}{os.sep}{simv_dic['name']}"
        ms_file = "simv_makefile"
        os.makedirs(ms_dir, exist_ok=True)
        LOG.info("simv dir %s is generated", ms_dir)
        pcom.ren_tempfile(
            f"{self.ced['PJ_TEMPLATES']}{os.sep}{ms_file}", f"{ms_dir}{os.sep}{ms_file}", ms_dic)
        return ms_dir, ms_file
    def gen_case_makefile(self, case_dic):
        """to generate case makefile"""
        mc_dic = {"CED": self.ced, "case_dic": case_dic, "ed": {
            "case": case_dic["name"], "seed": case_dic["seed"]}}
        mc_dic["clib_flg"] = self.mkg_dic["clib_flg"]
        mc_dir = f"{self.ced['MODULE_OUTPUT']}{os.sep}{case_dic['name']}{os.sep}{case_dic['seed']}"
        mc_file = "case_makefile"
        os.makedirs(mc_dir, exist_ok=True)
        LOG.info("case dir %s is generated", mc_dir)
        pcom.ren_tempfile(
            f"{self.ced['PJ_TEMPLATES']}{os.sep}{mc_file}", f"{mc_dir}{os.sep}{mc_file}", mc_dic)
        return mc_dir, mc_file
    def gen_simv_dic_dic(self):
        """to generate nested simv dic to support regression"""
        simv_dic_dic = collections.OrderedDict()
        for v_n in self.simv_set:
            if v_n not in self.cfg_dic["simv"]:
                continue
            if self.mkg_dic["regr_flg"]:
                self.cfg_dic["simv"][v_n].update(self.cfg_dic["proj"]["regression_simv"])
            self.cfg_dic["simv"][v_n].update(self.mkg_dic["ow_dic"]["ae"])
            simv_dic_dic[v_n] = self.gen_simv_dic(v_n)
        return simv_dic_dic
    def gen_case_dic_dic(self):
        """to generate nested case dic to support regression"""
        case_dic_dic = collections.OrderedDict()
        for c_n in self.cfg_dic["case"]:
            if c_n == "DEFAULT":
                continue
            if self.mkg_dic["regr_flg"]:
                self.cfg_dic["case"][c_n].update(self.cfg_dic["proj"]["regression_case"])
            self.cfg_dic["case"][c_n].update(self.mkg_dic["ow_dic"]["su"])
            case_dic_dic[c_n] = self.gen_case_dic(c_n)
        return case_dic_dic
