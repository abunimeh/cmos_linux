# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: EnvBooter class for booting inital env variables

### modules
import pcom
import os
import datetime as dt
import subprocess
import copy

### functions
def find_proj_root(path_str):
    if path_str == '/':
        raise Exception("it's not in a working copy from a project repository")
    elif os.path.isfile(path_str+os.sep+'.cas_proj_root_flg'):
        return path_str
    else:
        return find_proj_root(os.path.dirname(path_str))

def find_module_dir(ced, cfg_dic, module):
    for module_dir in pcom.find_iter(ced['PROJ_VERIF'], module, True):
        if os.path.isdir(module_dir+os.sep+'config'):
            return module_dir
            break
    else:
        tree_ignore_str = '|'.join(pcom.rd_cfg(
            cfg_dic['proj'], 'proj_module', 'tree_ignore'))
        run_str = 'tree -d -I "(|{0}|)" {1}'.format(
            tree_ignore_str, ced['PROJ_VERIF'])
        tree_str = subprocess.run(run_str, shell=True, check=True,
                                  stdout=subprocess.PIPE).stdout.decode()
        raise Exception("module {0} is NA; the possible module is {1}{2}"
                        "".format(module, os.linesep, tree_str))

### classes
class EnvBooter(object):
    def __init__(self, sim_module, LOG=None):
        self.LOG = LOG if LOG else pcom.gen_logger()
        self.sim_module = sim_module
        os.environ['PROJ_ROOT'] = find_proj_root(os.getcwd())
        os.environ['MODULE'] = sim_module
        self.ced = {'MODULE': sim_module, 'TIME': dt.datetime.now(),
                    'PROJ_ROOT': os.environ['PROJ_ROOT'],
                    'USER_NAME': os.environ['USER']}
        self.cfg_dic = {}
    def boot_env(self):
        proj_cfg = os.path.expandvars('$PROJ_ROOT/share/cmn/config/proj.cfg')
        if not os.path.isfile(proj_cfg):
            raise Exception("proj config file {0} is NA".format(proj_cfg))
        self.cfg_dic['proj'] = pcom.gen_cfg([proj_cfg])
        for env_key, env_value in self.cfg_dic['proj']['boot_env'].items():
            os.environ[env_key] = os.path.expandvars(env_value)
            self.ced[env_key] = os.path.expandvars(env_value)
        module_dir = find_module_dir(self.ced, self.cfg_dic, self.sim_module)
        os.environ['PROJ_MODULE'] = module_dir
        self.ced['PROJ_MODULE'] = module_dir
        for env_key, env_value in self.cfg_dic['proj']['proj_env'].items():
            os.environ[env_key] = os.path.expandvars(env_value)
            self.ced[env_key] = os.path.expandvars(env_value)
        group_cfg = self.ced['MODULE_CONFIG']+os.sep+'group.cfg'
        if not os.path.isfile(group_cfg):
            raise Exception("group config file {0} is NA".format(case_cfg))
        self.cfg_dic['group'] = pcom.gen_cfg([group_cfg])
        case_cfg = self.ced['MODULE_CONFIG']+os.sep+'case.cfg'
        if not os.path.isfile(case_cfg):
            raise Exception("case config file {0} is NA".format(case_cfg))
        self.cfg_dic['case'] = pcom.gen_cfg([case_cfg])
        group_proj_env = copy.copy(self.cfg_dic['proj']['env_group'])
        case_proj_env = copy.copy(self.cfg_dic['proj']['env_case'])
        group_proj_env.update(self.cfg_dic['group']['DEFAULT'])
        case_proj_env.update(self.cfg_dic['case']['DEFAULT'])
        self.cfg_dic['group']['DEFAULT'] = group_proj_env
        self.cfg_dic['case']['DEFAULT'] = case_proj_env
        return (self.ced, self.cfg_dic)
