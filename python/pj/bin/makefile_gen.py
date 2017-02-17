# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: MakefileGen class for sim/regr simv/case makefile generation

### modules
import pcom
import env_booter
import filelst_gen
import os
import jinja2
import random
import json
import pickle
import collections

### functions
def check_seed(seed, seed_set):
    if seed in seed_set:
        return check_seed(seed+1, seed_set)
    else:
        return seed

### classes
class MakefileGen(object):
    def __init__(self, LOG, ced, cfg_dic, ow_dic, cc_opts='',
                 regr_flg=False, fresh_flg=False):
        self.LOG = LOG if LOG else pcom.gen_logger()
        self.ced = ced
        self.cfg_dic = cfg_dic
        self.ow_dic = ow_dic
        self.simv_set = {'DEFAULT'}
        self.cc_opts = cc_opts
        self.regr_flg = regr_flg
        self.fresh_flg = fresh_flg
        self.vip_dep_file_lst = list(
            pcom.find_iter(self.ced['PROJ_VERIF']+os.sep+'vip', '*.sv'))
        self.templateLoader = jinja2.FileSystemLoader(self.ced['PJ_TEMPLATES'])
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)
    def rd_cfg(self, cfg_key, sec, opt):
        return pcom.rd_cfg(self.cfg_dic[cfg_key], sec, opt)
    def chk_simv_cfg(self, vn):
        vn_cfg = self.cfg_dic['simv'][vn]
        vg_dir = self.ced['OUTPUT_SIMV']+os.sep+vn
        simv_cfg_json = vg_dir+os.sep+'simv_cfg.json'
        os.makedirs(vg_dir, exist_ok=True)
        ojson = {}
        if os.path.isfile(simv_cfg_json):
            with open(simv_cfg_json) as jf:
                ojson = json.load(jf)
        self.cfg_dic['simv']['DEFAULT'].update(vn_cfg)
        njson = dict(self.cfg_dic['simv']['DEFAULT'])
        if ojson != njson or self.fresh_flg:
            with open(simv_cfg_json, 'w') as jf:
                json.dump(njson, jf)
    def gen_smf_lst(self, vn):
        smf_lst = []
        for sm in self.rd_cfg('simv', vn, 'sub_modules'):
            if not ':' in sm:
                raise Exception(
                    "sub_modules {0} in module {1} simv cfg has incorrect "
                    "name:type format".format(sm, self.ced['MODULE']))
            m_name, m_type, *_ = sm.split(':')
            module_dir = env_booter.find_module_dir(
                self.ced, self.cfg_dic, m_name)
            sm_flist = os.sep.join([module_dir, 'flist', m_type+'.flist'])
            if not os.path.isfile(sm_flist):
                raise Exception("sub_modules {0} has no such file {1}".format(
                    sm, sm_flist))
            smf_lst.append(sm_flist)
        return smf_lst
    def chk_simv_flist(self, vn, f_tup, tb_flg=False):
        gf_dir = self.ced['OUTPUT_SIMV']+os.sep+vn
        fn_str = 'simv_tbfl.pcl' if tb_flg else 'simv_dutfl.pcl'
        simv_flist_pcl = gf_dir+os.sep+fn_str
        os.makedirs(gf_dir, exist_ok=True)
        opcl = ()
        if os.path.isfile(simv_flist_pcl):
            with open(simv_flist_pcl, 'rb') as pf:
                opcl = pickle.load(pf)
        npcl = f_tup
        if opcl != npcl:
            with open(simv_flist_pcl, 'wb') as pf:
                pickle.dump(npcl, pf)
    def gen_simv_dic(self, vn):
        self.chk_simv_cfg(vn)
        simv_dic = {'name': vn}
        ca_opts_lst = self.rd_cfg('simv', vn, 'custom_ana_opts')
        ce_opts_lst = self.rd_cfg('simv', vn, 'custom_elab_opts')
        if self.regr_flg:
            ca_opts_lst = self.rd_cfg(
                'proj', 'regression_opts', 'custom_ana_opts')+ca_opts_lst
            ce_opts_lst = self.rd_cfg(
                'proj', 'regression_opts', 'custom_elab_opts')+ce_opts_lst
        cov_ce_lst = (self.rd_cfg('simv', vn, 'cov_elab_opts') if
                      self.rd_cfg('simv', vn, 'cov') == ['on'] else [])
        wf_lst = self.rd_cfg('simv', vn, 'wave_format')
        simv_dic['wave_format'] = 'fsdb' if not wf_lst else wf_lst[0]
        wave_ce_lst = (self.rd_cfg('simv', vn, 'wave_elab_opts')+
                       self.rd_cfg('simv', vn, 'wf_{0}_elab_opts'.format(
                           simv_dic['wave_format'])) if
                       self.rd_cfg('simv', vn, 'wave') == ['on'] else [])
        gui_ce_lst = (self.rd_cfg('simv', vn, 'gui_elab_opts') if
                      self.rd_cfg('simv', vn, 'gui') == ['on'] else [])
        prof_ce_lst = (self.rd_cfg('simv', vn, 'prof_elab_opts') if
                       self.rd_cfg('simv', vn, 'prof') == ['on'] else [])
        fpga_ca_lst = (self.rd_cfg('simv', vn, 'fpga_ana_opts') if
                       self.rd_cfg('simv', vn, 'fpga') == ['on'] else [])
        simv_dic['ca_opts'] = ' '.join(ca_opts_lst+fpga_ca_lst)
        simv_dic['ce_opts'] = ' '.join(
            ce_opts_lst+cov_ce_lst+wave_ce_lst+gui_ce_lst+prof_ce_lst)
        dut_flist_lst = ([self.ced['MODULE_FLIST']+os.sep+'rtl.flist'] +
                         self.gen_smf_lst(vn))
        df_tup = filelst_gen.FilelstGen(self.LOG).gen_file_lst(dut_flist_lst)
        (simv_dic['dut_dir_lst'], simv_dic['dut_file_lst'],
         simv_dic['vhdl_file_lst']) = df_tup
        self.chk_simv_flist(vn, df_tup, False)
        tb_flist_lst = [self.ced['MODULE_FLIST']+os.sep+'tb.flist']
        tf_tup = filelst_gen.FilelstGen(self.LOG).gen_file_lst(tb_flist_lst)
        simv_dic['tb_dir_lst'], simv_dic['tb_file_lst'], _ = tf_tup
        self.chk_simv_flist(vn, tf_tup, True)
        simv_dic['tb_dep_file_lst'] = self.vip_dep_file_lst + list(
            pcom.find_iter(self.ced['MODULE_TB'], '*.sv*'))
        vhdl_tool_lst = self.rd_cfg('simv', vn, 'vhdl_tool')
        simv_dic['vhdl_tool'] = (
            vhdl_tool_lst[0] if vhdl_tool_lst else 'vhdlan')
        simv_dic['vhdl_da_opts'] = ' '.join(self.rd_cfg(
            'simv', vn, 'vt_{0}_dut_ana_opts'.format(simv_dic['vhdl_tool'])))
        simv_dic['vhdl_ta_opts'] = ' '.join(self.rd_cfg(
            'simv', vn, 'vt_{0}_tb_ana_opts'.format(simv_dic['vhdl_tool'])))
        ana_tool_lst = self.rd_cfg('simv', vn, 'ana_tool')
        simv_dic['ana_tool'] = ana_tool_lst[0] if ana_tool_lst else 'vlogan'
        simv_dic['da_opts'] = ' '.join(self.rd_cfg(
            'simv', vn, 'at_{0}_dut_ana_opts'.format(simv_dic['ana_tool'])))
        simv_dic['ta_opts'] = ' '.join(self.rd_cfg(
            'simv', vn, 'at_{0}_tb_ana_opts'.format(simv_dic['ana_tool'])))
        elab_tool_lst = self.rd_cfg('simv', vn, 'elab_tool')
        simv_dic['elab_tool'] = elab_tool_lst[0] if elab_tool_lst else 'vcs'
        simv_dic['e_opts'] = ' '.join(self.rd_cfg(
            'simv', vn, 'et_{0}_elab_opts'.format(simv_dic['elab_tool'])))
        simv_dic['w_opts'] = ' '.join(self.rd_cfg('simv', vn, 'verdi_opts'))
        tb_top_lst = self.rd_cfg('simv', vn, 'tb_top')
        simv_dic['tb_top'] = tb_top_lst[0] if tb_top_lst else 'test_top'
        simv_dic['pre_cmd_lst'] = self.rd_cfg('simv', vn, 'pre_cmd')
        simv_dic['post_cmd_lst'] = self.rd_cfg('simv', vn, 'post_cmd')
        simv_dic['file_dic'] = {}
        for opt_name, opt_cont in self.cfg_dic['simv'][vn].items():
            if not opt_name.startswith('file__'):
                continue
            simv_dic['file_dic'][opt_name[6:]] = opt_cont.replace(
                '$', '$$').replace('\\', '').split(os.linesep)
        return simv_dic
    def gen_case_dic(self, cn):
        case_dic = {'name': cn}
        simv_lst = self.rd_cfg('case', cn, 'simv')
        case_dic['simv'] = (simv_lst[0] if simv_lst and simv_lst[0] in
                             self.cfg_dic['simv'] else 'DEFAULT')
        self.simv_set.add(case_dic['simv'])
        tb_top_lst = self.rd_cfg('simv', case_dic['simv'], 'tb_top')
        case_dic['tb_top'] = tb_top_lst[0] if tb_top_lst else 'test_top'
        case_dic['wave'] = True if self.rd_cfg(
            'case', cn, 'wave') == ['on'] else False
        wf_lst = self.rd_cfg('simv', case_dic['simv'], 'wave_format')
        case_dic['wave_format'] = 'fsdb' if not wf_lst else wf_lst[0]
        case_dic['wave_mem'] = True if self.rd_cfg(
            'case', cn, 'wave_mem') == ['on'] else False
        case_dic['wave_glitch'] = True if self.rd_cfg(
            'case', cn, 'wave_glitch') == ['on'] else False
        su_opts_lst = self.rd_cfg('case', cn, 'custom_simu_opts')
        if self.regr_flg:
            su_opts_lst = self.rd_cfg(
                'proj', 'regression_opts', 'custom_simu_opts')+su_opts_lst
        cov_su_lst = (self.rd_cfg('case', cn, 'cov_simu_opts') if
                      self.rd_cfg('case', cn, 'cov') == ['on'] else [])
        wave_su_lst = (self.rd_cfg('case', cn, 'wf_{0}_simu_opts'.format(
            case_dic['wave_format'])) if
                       self.rd_cfg('case', cn, 'wave') == ['on'] else [])
        wg_su_lst = (self.rd_cfg('case', cn, 'wf_{0}_glitch_simu_opts'.format(
            case_dic['wave_format'])) if
                     self.rd_cfg('case', cn, 'wave') == ['on'] and
                     self.rd_cfg('case', cn, 'wave_glitch') == ['on'] else [])
        seed_su_lst = self.rd_cfg('case', cn, 'seed_simu_opts')
        uvm_su_lst = (self.rd_cfg('case', cn, 'uvm_simu_opts') if
                      self.rd_cfg('case', cn, 'uvm') == ['on'] else [])
        gui_su_lst = (self.rd_cfg('case', cn, 'gui_simu_opts') if
                      self.rd_cfg('case', cn, 'gui') == ['on'] else [])
        prof_mem_su_lst = (
            self.rd_cfg('case', cn, 'prof_mem_simu_opts') if
            self.rd_cfg('case', cn, 'prof_mem') == ['on'] else [])
        prof_time_su_lst = (
            self.rd_cfg('case', cn, 'prof_time_simu_opts') if
            self.rd_cfg('case', cn, 'prof_time') == ['on'] else [])
        case_dic['su_opts'] = ' '.join(
            su_opts_lst+cov_su_lst+wave_su_lst+wg_su_lst+seed_su_lst+
            uvm_su_lst+gui_su_lst+prof_mem_su_lst+prof_time_su_lst)
        case_dic['w_opts'] = ' '.join(self.rd_cfg(
            'simv', case_dic['simv'], 'verdi_opts'))
        case_dic['pre_cmd_lst'] = self.rd_cfg('case', cn, 'pre_cmd')
        case_dic['post_cmd_lst'] = self.rd_cfg('case', cn, 'post_cmd')
        case_dic['file_dic'] = {}
        for opt_name, opt_cont in self.cfg_dic['case'][cn].items():
            if not opt_name.startswith('file__'):
                continue
            case_dic['file_dic'][opt_name[6:]] = opt_cont.replace(
                '$', '$$').replace('\\', '').split(os.linesep)
        case_dic['regr_type_lst'] = self.rd_cfg('case', cn, 'regression_type')
        case_dic['regr_type_lst'].append('all')
        seed_set = set()
        seed_lst = self.rd_cfg('case', cn, 'seed')
        rt_lst = self.rd_cfg('case', cn, 'random_times')
        loop_times = rt_lst[0] if rt_lst and rt_lst[0].isdigit() else '1'
        for i in range(int(loop_times)):
            if rt_lst:
                seed = check_seed(random.randrange(1, 999999), seed_set)
                seed_set.add(seed)
            elif seed_lst:
                if seed_lst[0].isdigit():
                    seed_set.add(int(seed_lst[0]))
                else:
                    seed = check_seed(random.randrange(1, 999999), seed_set)
                    seed_set.add(seed)
            else:
                seed_set.add(1)
        case_dic['seed_set'] = seed_set
        return case_dic
    def gen_makefile(self):
        mk_dic = {'CED': self.ced}
        mk_dic['c_lst'] = [
            os.path.basename(os.path.splitext(cc)[0]) for cc in pcom.find_iter(
                self.ced['MODULE_C'], '*.c', cur_flg=True) if
            cc] if os.path.isdir(self.ced['MODULE_C']) else []
        mk_dic['c_opts'] = self.cc_opts if self.cc_opts else ' '.join(
            self.rd_cfg('proj', 'proj', 'c_opts'))
        template = self.templateEnv.get_template('Makefile')
        template_out = template.render(mk_dic)
        mk_dir = self.ced['MODULE_OUTPUT']
        os.makedirs(mk_dir, exist_ok=True)
        self.LOG.info("output dir {0} is generated".format(mk_dir))
        mk_file = 'Makefile'
        with open(mk_dir+os.sep+mk_file, 'w') as f:
            f.write(template_out)
        return (mk_dir, mk_file)
    def gen_simv_makefile(self, simv_dic):
        ms_dic = {'CED': self.ced, 'simv_dic': simv_dic,
                  'ed': {'simv': simv_dic['name']}}
        ms_dic['c_lst'] = [
            os.path.basename(os.path.splitext(cc)[0]) for cc in pcom.find_iter(
                self.ced['MODULE_C'], '*.c', cur_flg=True) if
            cc] if os.path.isdir(self.ced['MODULE_C']) else []
        template = self.templateEnv.get_template('simv_makefile')
        template_out = template.render(ms_dic)
        ms_dir = self.ced['OUTPUT_SIMV']+os.sep+simv_dic['name']
        os.makedirs(ms_dir, exist_ok=True)
        self.LOG.info("simv dir {0} is generated".format(ms_dir))
        ms_file = 'simv_makefile'
        with open(ms_dir+os.sep+ms_file, 'w') as f:
            f.write(template_out)
        return (ms_dir, ms_file)
    def gen_case_makefile(self, case_dic):
        mc_dic = {'CED': self.ced, 'case_dic': case_dic,
                  'ed': {'case': case_dic['name'], 'seed': case_dic['seed']}}
        template = self.templateEnv.get_template('case_makefile')
        template_out = template.render(mc_dic)
        mc_dir = self.ced[
            'MODULE_OUTPUT']+os.sep+case_dic['name']+os.sep+case_dic['seed']
        os.makedirs(mc_dir, exist_ok=True)
        self.LOG.info("case dir {0} is generated".format(mc_dir))
        mc_file = 'case_makefile'
        with open(mc_dir+os.sep+mc_file, 'w') as f:
            f.write(template_out)
        return (mc_dir, mc_file)
    def gen_simv_dic_dic(self):
        simv_dic_dic = collections.OrderedDict()
        for vn in self.simv_set:
            if vn not in self.cfg_dic['simv']:
                continue
            if self.regr_flg:
                self.cfg_dic['simv'][vn].update(
                    self.cfg_dic['proj']['regression_simv'])
            self.cfg_dic['simv'][vn].update(self.ow_dic['ae'])
            simv_dic_dic[vn] = self.gen_simv_dic(vn)
        return simv_dic_dic
    def gen_case_dic_dic(self):
        case_dic_dic = collections.OrderedDict()
        for cn in self.cfg_dic['case']:
            if cn == 'DEFAULT':
                continue
            if self.regr_flg:
                self.cfg_dic['case'][cn].update(
                    self.cfg_dic['proj']['regression_case'])
            self.cfg_dic['case'][cn].update(self.ow_dic['su'])
            case_dic_dic[cn] = self.gen_case_dic(cn)
        return case_dic_dic
