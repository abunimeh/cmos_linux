"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: pj run sub cmd entrence and simulation flows class
"""

import os
import json
import datetime as dt
import subprocess
import texttable
import pcom
import env_booter
import makefile_gen
import fpga_signals_gen
import sim_log_parser

LOG = pcom.gen_logger(__name__)

class SRProc(object):
    """simulation and regression processor for pj"""
    def __init__(self, run_dic):
        if not run_dic["module"]:
            run_dic["module"] = run_dic["case_lst"][0].split("__")[0]
        if not run_dic["module"]:
            raise Exception(
                f"case {run_dic['case_lst'][0]} is not in standard format <module__case>, "
                f"so module name must be specified")
        run_dic["case_lst"] = [cc.split(".")[0] for cc in run_dic["case_lst"] if cc]
        self.ced, self.cfg_dic = env_booter.EnvBooter(
            {"x86_ins_flg": run_dic["x86_ins"],
             "x86_ins_num": run_dic["x86_ins_num"],
             "x86_ins_groups": run_dic["x86_ins_groups"]}).module_env(run_dic["module"])
        if run_dic["list"]:
            run_dic["x86_ins"] = False
        self.regr_flg = regr_flg = True if run_dic["regr_type_lst"] else False
        self.std = subprocess.PIPE if regr_flg else None
        self.ow_dic = {"pre": {}, "ae": {}, "su": {}}
        self.run_dic = run_dic
    def gen_ow_dic_opts(self):
        """to generate overwirte dic for options"""
        if self.run_dic["lib_comp_opts"]:
            self.ow_dic["pre"]["lib_comp_opts"] = self.run_dic["lib_comp_opts"].strip()
        if self.run_dic["src_comp_opts"]:
            self.ow_dic["pre"]["src_comp_opts"] = self.run_dic["src_comp_opts"].strip()
        if self.run_dic["src_run_opts"]:
            self.ow_dic["pre"]["src_run_opts"] = self.run_dic["src_run_opts"].strip()
        if self.run_dic["dut_ana_opts"]:
            self.ow_dic["ae"]["custom_dut_ana_opts"] = self.run_dic["dut_ana_opts"].strip()
        if self.run_dic["tb_ana_opts"]:
            self.ow_dic["ae"]["custom_tb_ana_opts"] = self.run_dic["tb_ana_opts"].strip()
        if self.run_dic["elab_opts"]:
            self.ow_dic["ae"]["custom_elab_opts"] = self.run_dic["elab_opts"].strip()
        if self.run_dic["simu_opts"]:
            self.ow_dic["su"]["custom_simu_opts"] = self.run_dic["simu_opts"].strip()
    def gen_ow_dic_nopts1(self):
        """to generate overwrite dic for non options part 1"""
        if self.run_dic["seed"]:
            self.ow_dic["su"]["seed"] = self.run_dic["seed"].strip()
        if self.run_dic["wave"] != None:
            self.ow_dic["ae"]["wave"] = "on"
            self.ow_dic["su"]["wave"] = "on"
            if "mem" in self.run_dic["wave"]:
                self.ow_dic["su"]["wave_mem"] = "on"
            if "glitch" in self.run_dic["wave"]:
                self.ow_dic["su"]["wave_glitch"] = "on"
        if self.run_dic["rt"]:
            self.ow_dic["su"]["random_times"] = self.run_dic["rt"].strip()
        if self.run_dic["prof"]:
            self.ow_dic["ae"]["prof"] = "on"
            if "time" in self.run_dic["prof"]:
                self.ow_dic["su"]["prof_time"] = "on"
            if "mem" in self.run_dic["prof"]:
                self.ow_dic["su"]["prof_mem"] = "on"
    def gen_ow_dic_nopts2(self):
        """to generate overwrite dic for non options part 2"""
        if self.run_dic["verdi"]:
            self.ow_dic["ae"]["wave"] = "on"
            self.ow_dic["su"]["wave"] = "on"
        if self.run_dic["gui"]:
            self.ow_dic["ae"]["gui"] = "on"
            self.ow_dic["su"]["gui"] = "on"
        if self.run_dic["cov"]:
            self.ow_dic["ae"]["cov"] = "on"
            self.ow_dic["su"]["cov"] = "on"
        if self.run_dic["upf"]:
            self.ow_dic["ae"]["upf"] = "on"
        if self.run_dic["fpga"]:
            self.ow_dic["ae"]["fpga"] = "on"
    @classmethod
    def update_status(cls, case_dic):
        """to update case simulation status"""
        if case_dic["simu_status"] == "passed" and case_dic[
                "elab_status"] == "passed" and case_dic[
                    "tb_ana_status"] == "passed" and case_dic[
                        "dut_ana_status"] == "passed":
            case_dic["status"] = case_dic["simu_status"]
            case_dic["estage"] = "NA"
            case_dic["einfo"] = case_dic["simu_error"]
        elif case_dic["elab_status"] == "passed" and case_dic[
                "tb_ana_status"] == "passed" and case_dic[
                    "dut_ana_status"] == "passed":
            case_dic["status"] = case_dic["simu_status"]
            case_dic["estage"] = "simulation"
            case_dic["einfo"] = case_dic["simu_error"]
        elif case_dic["tb_ana_status"] == "passed" and case_dic[
                "dut_ana_status"] == "passed":
            case_dic["status"] = case_dic["elab_status"]
            case_dic["estage"] = "elaboration"
            case_dic["einfo"] = case_dic["elab_error"]
        elif case_dic["dut_ana_status"] == "passed":
            case_dic["status"] = case_dic["tb_ana_status"]
            case_dic["estage"] = "tb analysis"
            case_dic["einfo"] = case_dic["tb_ana_error"]
        else:
            case_dic["status"] = case_dic["dut_ana_status"]
            case_dic["estage"] = "dut analysis"
            case_dic["einfo"] = case_dic["dut_ana_error"]
        return case_dic
    def gen_x86_ins(self):
        """to invoke test_gen to generate x86 ins case"""
        scr_xi_dir = f"{self.ced['SHARE_SCRIPTS']}{os.sep}X86_INS"
        ins_gen_file = f"{scr_xi_dir}{os.sep}ins_gen.py"
        if not os.path.isfile(ins_gen_file):
            raise Exception(f"ins_gen.py file {ins_gen_file} is NA")
        test_gen_file = f"{scr_xi_dir}{os.sep}test_gen.pl"
        if not os.path.isfile(test_gen_file):
            raise Exception(f"test_gen.pl file {test_gen_file} is NA")
        cfg_lst = list(pcom.find_iter(self.ced["MODULE_CONFIG"], "case_*.cfg"))
        input_seed = self.ow_dic["su"].get("seed", "")
        seed_str = input_seed if input_seed.isdigit() else "random"
        os.sys.path.append(scr_xi_dir)
        import ins_gen
        x86_ins_seed_dic = ins_gen.InsGen(
            LOG, cfg_lst, self.run_dic["case_lst"], seed=seed_str, path=self.ced["PROJ_MODULE"],
            regr_types=self.run_dic["regr_type_lst"]).gen_ins()
        subprocess.run(
            (f"perl {test_gen_file} test_name= seed=1 inst_mod=16 sfile_type=asm "
             f"input={self.ced['MODULE_OUTPUT']} output={self.ced['MODULE_OUTPUT']}"),
            shell=True, check=True)
        return x86_ins_seed_dic
    def proc_simv(self, mkg):
        """to process simv related steps"""
        simv_dic_dic = mkg.gen_simv_dic_dic()
        for simv, simv_dic in simv_dic_dic.items():
            ms_dir, ms_file = mkg.gen_simv_makefile(simv_dic)
            ms_tar = ""
            if self.run_dic["comp"]:
                ms_tar += f"{self.ced['OUTPUT_SIMV']}{os.sep}{simv}{os.sep}simv "
            if self.run_dic["verdi"] and not self.run_dic["case_lst"]:
                ms_tar += f"verdi_{simv} "
            if not (ms_tar or self.run_dic["case_lst"]):
                ms_tar = f"{self.ced['OUTPUT_SIMV']}{os.sep}{simv}{os.sep}.dut_ana "
            ms_str = f"cd {ms_dir} && make -f {ms_file} {ms_tar}"
            subprocess.run(ms_str, shell=True, check=True, stdout=self.std, stderr=self.std)
    def proc_sin_case(self, case_dic, sc_dic):
        """to process single case step"""
        case_dic["seed"] = sc_dic["seed"]
        case_dir = os.path.join(self.ced["MODULE_OUTPUT"], case_dic["name"], case_dic["seed"])
        os.makedirs(case_dir, exist_ok=True)
        with open(f"{case_dir}{os.sep}case_info.json", "w") as cjf:
            json.dump(
                {"pub_date": dt.datetime.timestamp(self.ced["TIME"]),
                 "c_name": case_dic["name"],
                 "v_name": case_dic["simv"],
                 "m_name": self.ced["MODULE"],
                 "proj_name": self.ced["PROJ_NAME"],
                 "user_name": self.ced["USER_NAME"],
                 "seed": case_dic["seed"]}, cjf)
        mc_dir, mc_file = sc_dic["mkg"].gen_case_makefile(case_dic)
        mc_tar = f"run_simv_{case_dic['name']}__{case_dic['seed']} "
        if self.run_dic["verdi"]:
            verdi_tar = f"verdi_{case_dic['name']}__{case_dic['seed']} "
            mc_tar = f"{mc_tar}{verdi_tar}" if self.run_dic["wave"] != None else verdi_tar
        mc_str = f"cd {mc_dir} && make -f {mc_file} {mc_tar}"
        if self.regr_flg:
            subprocess.run(mc_str, shell=True, check=True, stdout=self.std, stderr=self.std)
        else:
            proc = subprocess.Popen(mc_str, shell=True)
            try:
                proc.communicate()
            except KeyboardInterrupt:
                proc.communicate()
                return
        cvsr_tup = (
            case_dic["name"], case_dic["simv"], case_dic["seed"], self.run_dic["regr_type_lst"])
        if self.run_dic["fpga"]:
            sc_dic["fsg"].gen_fpga_signals(cvsr_tup)
        case_log_dic = self.update_status(
            sim_log_parser.LogParser(self.ced, self.cfg_dic, cvsr_tup).parse_log())
        if self.regr_flg:
            log_str = (
                f"Case Name: {case_log_dic['c_name']}{os.linesep}{' '*16}"
                f"Seed: {case_log_dic['seed']}{os.linesep}{' '*16}"
                f"Status: {case_log_dic['status']}{os.linesep}{' '*16}"
                f"Error Stage: {case_log_dic['estage']}")
            if case_log_dic["status"] == "passed":
                LOG.info(log_str)
            else:
                LOG.error(log_str)
        return case_log_dic
    def proc_case(self, mkg, case_dic_dic):
        """to process case related steps"""
        if self.run_dic["case_lst"]:
            if self.run_dic["x86_ins"]:
                x86_ins_seed_dic = self.gen_x86_ins()
            sc_dic = {"mkg": mkg}
            if self.run_dic["fpga"]:
                fsg = fpga_signals_gen.FPGASignalsGen(self.ced)
                fsg.gen_h_lst()
                sc_dic["fsg"] = fsg
            rpt_dic = {
                "rows": [
                    ["Case Name", "Case Simv", "SVN CL", "Seed", "Status",
                     "Error Stage", "CPU Time"]],
                "dic_lst": [],
                "file": f"{self.ced['MODULE_OUTPUT']}{os.sep}run_rpt",
                "jf": f"{self.ced['MODULE_OUTPUT']}{os.sep}run_status.json"}
            for case in self.run_dic["case_lst"]:
                if case not in case_dic_dic:
                    continue
                case_dic = case_dic_dic[case]
                if self.regr_flg:
                    if not any([cc in case_dic["regr_type_lst"] for cc in self.run_dic[
                            "regr_type_lst"] if cc]):
                        continue
                if self.run_dic["x86_ins"] and case in x86_ins_seed_dic:
                    case_dic["seed_set"] = {x86_ins_seed_dic[case]}
                for seed in case_dic["seed_set"]:
                    seed = str(seed)
                    if self.run_dic["failed_mode"]:
                        if os.path.isfile(os.path.join(
                                self.ced["MODULE_OUTPUT"], case, seed, "case_passed")):
                            continue
                    sc_dic["seed"] = seed
                    case_log_dic = self.proc_sin_case(case_dic, sc_dic)
                    if case_log_dic is None:
                        break
                    rpt_dic["rows"].append(
                        [case_log_dic["c_name"],
                         case_log_dic["v_name"],
                         case_log_dic["proj_cl"],
                         case_log_dic["seed"],
                         case_log_dic["status"],
                         case_log_dic["estage"],
                         f"{case_log_dic['simu_cpu_time']}s"])
                    rpt_dic["dic_lst"].append(
                        {"case": case_log_dic["c_name"],
                         "seed": case_log_dic["seed"],
                         "status": case_log_dic["status"]})
            table = texttable.Texttable()
            table.set_cols_width([30, 7, 7, 7, 7, 7, 7])
            table.add_rows(rpt_dic["rows"])
            sim_table = table.draw()
            LOG.info(f"run report table:{os.linesep}{sim_table}")
            with open(rpt_dic["file"], "w") as rpf:
                rpf.write(sim_table)
            with open(rpt_dic["jf"], "w")  as rjf:
                json.dump(rpt_dic["dic_lst"], rjf)
            LOG.info("run report file %s", rpt_dic["file"])
    def proc_sr(self):
        """to process and kick off sim/regr flow"""
        self.gen_ow_dic_opts()
        self.gen_ow_dic_nopts1()
        self.gen_ow_dic_nopts2()
        mkg = makefile_gen.MakefileGen(self.ced, self.cfg_dic, {
            "ow_dic": self.ow_dic, "regr_flg": self.regr_flg, "fresh_flg": self.run_dic["fresh"]})
        case_dic_dic = mkg.gen_case_dic_dic()
        if self.run_dic["list"]:
            str_lst = [f"all cases of module {self.ced['MODULE']}"]
            str_lst.append("*"*30)
            str_lst += list(case_dic_dic)
            str_lst.append("*"*30)
            LOG.info(os.linesep.join(str_lst))
            return
        if self.run_dic["all"] or self.regr_flg:
            self.run_dic["case_lst"] = list(case_dic_dic)
        mk_dir, mk_file = mkg.gen_makefile()
        mk_tar = ""
        if self.run_dic["clib"]:
            mk_tar += "compile_clib "
        if self.run_dic["csrc"]:
            mk_tar += "run_csrc "
        if mk_tar:
            mk_str = f"cd {mk_dir} && make -f {mk_file} {mk_tar}"
            subprocess.run(mk_str, shell=True, check=True, stdout=self.std, stderr=self.std)
            LOG.info("compiling c code done")
            return
        self.proc_simv(mkg)
        self.proc_case(mkg, case_dic_dic)

def run_sr(args):
    """to run sim/regr cmd"""
    if args.run_module or args.run_case_lst or args.regr_type_lst:
        SRProc(
            {"module": args.run_module,
             "case_lst": args.run_case_lst,
             "regr_type_lst": args.regr_type_lst,
             "all": args.run_all,
             "comp": args.run_comp,
             "clib": args.run_clib,
             "csrc": args.run_csrc,
             "list": args.run_list,
             "wave": args.run_wave,
             "verdi": args.run_verdi,
             "gui": args.run_gui,
             "rt": args.run_rt,
             "cov": args.run_cov,
             "upf": args.run_upf,
             "prof": args.run_prof,
             "fpga": args.run_fpga,
             "fresh": args.run_fresh,
             "failed_mode": args.run_failed_mode,
             "x86_ins": args.run_x86_ins,
             "x86_ins_num": args.run_x86_ins_num,
             "x86_ins_groups": args.run_x86_ins_groups,
             "seed": args.run_seed,
             "lib_comp_opts": args.run_lib_comp_opts,
             "src_comp_opts": args.run_src_comp_opts,
             "src_run_opts": args.run_src_run_opts,
             "dut_ana_opts": args.run_dut_ana_opts,
             "tb_ana_opts": args.run_tb_ana_opts,
             "elab_opts": args.run_elab_opts,
             "simu_opts": args.run_simu_opts}).proc_sr()
        LOG.info("running module %s done", args.run_module)
    else:
        raise Exception("missing main arguments")
