"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: EnvBooter class for booting inital env variables
"""

import os
import datetime as dt
import subprocess
import copy
import pcom

LOG = pcom.gen_logger(__name__)

def find_proj_root(path_str):
    """to find project root directory according to specified file"""
    if path_str == "/":
        raise Exception("it's not in a working copy from a project repository")
    elif os.path.isfile(f"{path_str}{os.sep}{pcom.FLAG_FILE}"):
        return path_str
    else:
        return find_proj_root(os.path.dirname(path_str))

def find_module_dir(ced, cfg_dic, module):
    """to find verification module dir according to their subdir config"""
    for module_dir in pcom.find_iter(ced["PROJ_VERIF"], module, True):
        if os.path.isdir(f"{module_dir}{os.sep}config"):
            return module_dir
    tree_ignore_str = "|".join(pcom.rd_cfg(cfg_dic["proj"], "proj", "tree_ignore"))
    run_str = f"tree -d -I '(|{tree_ignore_str}|)' {ced['PROJ_VERIF']}"
    tree_str = subprocess.run(
        run_str, shell=True, check=True, stdout=subprocess.PIPE).stdout.decode()
    raise Exception(f"module {module} is NA; the possible module is {os.linesep}{tree_str}")

class EnvBooter(object):
    """environment booter for pj"""
    def __init__(self):
        self.ced = {}
        self.cfg_dic = {}
    def boot_env(self):
        """to boot top environments used only by pj"""
        os.environ["PROJ_ROOT"] = find_proj_root(os.getcwd())
        self.ced = {
            "PROJ_ROOT": os.environ["PROJ_ROOT"],
            "TIME": dt.datetime.now(),
            "USER_NAME": os.environ["USER"]}
        proj_cfg = os.path.expandvars("$PROJ_ROOT/share/config/proj.cfg")
        if not os.path.isfile(proj_cfg):
            raise Exception(f"proj config file {proj_cfg} is NA")
        self.cfg_dic = {"proj": pcom.gen_cfg([proj_cfg])}
        for env_key, env_value in (
                self.cfg_dic["proj"]["boot_env"] if "boot_env" in self.cfg_dic["proj"]
                else {}).items():
            os.environ[env_key] = os.path.expandvars(env_value)
            self.ced[env_key] = os.path.expandvars(env_value)
        return self.ced, self.cfg_dic
    def module_env(self, sim_module):
        """to boot verification module level environments used only by pj"""
        self.boot_env()
        self.ced["MODULE"] = os.environ["MODULE"] = sim_module
        self.ced["PROJ_MODULE"] = os.environ["PROJ_MODULE"] = find_module_dir(
            self.ced, self.cfg_dic, sim_module)
        for env_key, env_value in (
                self.cfg_dic["proj"]["module_env"] if "module_env" in self.cfg_dic["proj"]
                else {}).items():
            os.environ[env_key] = os.path.expandvars(env_value)
            self.ced[env_key] = os.path.expandvars(env_value)
        c_cfg = f"{self.ced['MODULE_CONFIG']}{os.sep}c.cfg"
        if not os.path.isfile(c_cfg):
            c_cfg = ""
        self.cfg_dic["c"] = pcom.gen_cfg([c_cfg])
        simv_cfg = f"{self.ced['MODULE_CONFIG']}{os.sep}simv.cfg"
        if not os.path.isfile(simv_cfg):
            raise Exception(f"simv config file {simv_cfg} is NA")
        self.cfg_dic["simv"] = pcom.gen_cfg([simv_cfg])
        case_cfg = f"{self.ced['MODULE_CONFIG']}{os.sep}case.cfg"
        if not os.path.isfile(case_cfg):
            raise Exception(f"case config file {case_cfg} is NA")
        case_cfg_lst = [case_cfg]
        for cfg_file in pcom.find_iter(self.ced["MODULE_CONFIG"], "case_*.cfg"):
            LOG.info("more case config file %s", cfg_file)
            case_cfg_lst.append(cfg_file)
        case_cfg_lst.reverse()
        self.cfg_dic["case"] = pcom.gen_cfg(case_cfg_lst)
        c_module_env = copy.copy(
            self.cfg_dic["proj"]["env_c"] if "env_c" in self.cfg_dic["proj"] else {})
        simv_module_env = copy.copy(
            self.cfg_dic["proj"]["env_simv"] if "env_simv" in self.cfg_dic["proj"] else {})
        case_module_env = copy.copy(
            self.cfg_dic["proj"]["env_case"] if "env_case" in self.cfg_dic["proj"] else {})
        c_module_env.update(self.cfg_dic["c"]["DEFAULT"])
        simv_module_env.update(self.cfg_dic["simv"]["DEFAULT"])
        case_module_env.update(self.cfg_dic["case"]["DEFAULT"])
        self.cfg_dic["c"]["DEFAULT"] = c_module_env
        self.cfg_dic["simv"]["DEFAULT"] = simv_module_env
        self.cfg_dic["case"]["DEFAULT"] = case_module_env
        return self.ced, self.cfg_dic
