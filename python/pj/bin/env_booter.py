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
            cfg_dic['proj'], 'proj', 'tree_ignore'))
        run_str = 'tree -d -I "(|{0}|)" {1}'.format(
            tree_ignore_str, ced['PROJ_VERIF'])
        tree_str = subprocess.run(run_str, shell=True, check=True,
                                  stdout=subprocess.PIPE).stdout.decode()
        raise Exception("module {0} is NA; the possible module is {1}{2}"
                        "".format(module, os.linesep, tree_str))

def boot_env():
    os.environ['PROJ_ROOT'] = find_proj_root(os.getcwd())
    ced = {'PROJ_ROOT': os.environ['PROJ_ROOT'],
           'TIME': dt.datetime.now(),
           'USER_NAME': os.environ['USER']}
    proj_cfg = os.path.expandvars('$PROJ_ROOT/share/config/proj.cfg')
    if not os.path.isfile(proj_cfg):
        raise Exception("proj config file {0} is NA".format(proj_cfg))
    cfg_dic = {'proj': pcom.gen_cfg([proj_cfg])}
    for env_key, env_value in cfg_dic['proj']['boot_env'].items():
        os.environ[env_key] = os.path.expandvars(env_value)
        ced[env_key] = os.path.expandvars(env_value)
    return (ced, cfg_dic)

def module_env(LOG, sim_module, x86_ins_flg=False,
               x86_ins_num=None, x86_ins_groups=None):
    LOG = LOG if LOG else pcom.gen_logger()
    ced, cfg_dic = boot_env()
    os.environ['MODULE'] = sim_module
    ced['MODULE'] = sim_module
    module_dir = find_module_dir(ced, cfg_dic, sim_module)
    os.environ['PROJ_MODULE'] = module_dir
    ced['PROJ_MODULE'] = module_dir
    for env_key, env_value in cfg_dic['proj']['module_env'].items():
        os.environ[env_key] = os.path.expandvars(env_value)
        ced[env_key] = os.path.expandvars(env_value)
    if x86_ins_flg:
        x86_ins_num = (int(
            pcom.rd_cfg(cfg_dic['proj'], 'x86_ins', 'default_ins_num')[0]) if
                       x86_ins_num == None else x86_ins_num)
        x86_ins_groups = (
            pcom.rd_cfg(cfg_dic['proj'], 'x86_ins', 'case_group') if
            x86_ins_groups == None else x86_ins_groups)
        scr_xi_dir = ced['SHARE_SCRIPTS']+os.sep+'X86_INS'
        case_gen_file = scr_xi_dir+os.sep+'case_gen.py'
        if not os.path.isfile(case_gen_file):
            raise Exception("case_gen.py file {0} is NA".format(case_gen_file))
        os.sys.path.append(scr_xi_dir)
        import case_gen
        for cg_name in x86_ins_groups:
            case_gen_inst = case_gen.CaseGen(
                ced['MODULE'], cg_name, x86_ins_num, ced['MODULE_CONFIG'])
            case_gen_inst.gen_case()
    simv_cfg = ced['MODULE_CONFIG']+os.sep+'simv.cfg'
    if not os.path.isfile(simv_cfg):
        raise Exception("simv config file {0} is NA".format(case_cfg))
    cfg_dic['simv'] = pcom.gen_cfg([simv_cfg])
    case_cfg = ced['MODULE_CONFIG']+os.sep+'case.cfg'
    if not os.path.isfile(case_cfg):
        raise Exception("case config file {0} is NA".format(case_cfg))
    case_cfg_lst = [case_cfg]
    for cfg_file in pcom.find_iter(ced['MODULE_CONFIG'], 'case_*.cfg'):
        LOG.info("more case config file {0}".format(cfg_file))
        case_cfg_lst.append(cfg_file)
    case_cfg_lst.reverse()
    cfg_dic['case'] = pcom.gen_cfg(case_cfg_lst)
    simv_module_env = copy.copy(cfg_dic['proj']['env_simv'])
    case_module_env = copy.copy(cfg_dic['proj']['env_case'])
    simv_module_env.update(cfg_dic['simv']['DEFAULT'])
    case_module_env.update(cfg_dic['case']['DEFAULT'])
    cfg_dic['simv']['DEFAULT'] = simv_module_env
    cfg_dic['case']['DEFAULT'] = case_module_env
    return (ced, cfg_dic)
