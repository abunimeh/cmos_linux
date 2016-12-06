# Author: Guanyu Yi @ CPU Verification Platform Group
# Email: yigy@cpu.com.cn
# Description: MakefileGen class for sim/regr makefile generation

### modules
import pcom
import env_booter
import filelst_gen
import os
import re
import jinja2
import copy
import random
import json
import pickle
import subprocess
import collections

### functions
def check_seed(seed, seed_set):
    if seed in seed_set:
        return check_seed(seed+1, seed_set)
    else:
        return seed

### classes
class MakefileGen(object):
    def __init__(self, LOG, ced, cfg_dic, ow_dic, case_lst=[], cc_opts='',
                 regr_flg=False, fresh_flg=False, x86_ins_flg=False,
                 all_case_flg=False):
        self.LOG = LOG if LOG else pcom.gen_logger()
        self.ced = ced
        self.cfg_dic = cfg_dic
        self.ow_dic = ow_dic
        self.case_lst = case_lst
        self.cc_opts = cc_opts
        self.regr_flg = regr_flg
        self.fresh_flg = fresh_flg
        self.x86_ins_flg = x86_ins_flg
        self.cvs_dic = collections.OrderedDict()
        self.regr_dic = collections.OrderedDict()
        self.vip_dep_file_lst = list(
            pcom.find_iter(self.ced['PROJ_VERIF']+os.sep+'vip', '*.sv'))
        if self.x86_ins_flg:
            scr_xi_dir = self.ced['CMN_SCRIPTS']+os.sep+'X86_INS'
            ins_gen_file = scr_xi_dir+os.sep+'ins_gen.py'
            if not os.path.isfile(ins_gen_file):
                raise Exception(
                    "ins_gen.py file {0} is NA".format(ins_gen_file))
            self.test_gen_file = scr_xi_dir+os.sep+'test_gen.pl'
            if not os.path.isfile(self.test_gen_file):
                raise Exception(
                    "test_gen.pl file {0} is NA".format(self.test_gen_file))
            self.cfg_lst = list(
                pcom.find_iter(self.ced['MODULE_CONFIG'], 'case_*.cfg'))
        self.all_case_flg = all_case_flg
    def rd_cfg(self, cfg_key, sec, opt):
        return pcom.rd_cfg(self.cfg_dic[cfg_key], sec, opt)
    def chk_simv_cfg(self, gn):
        gn_cfg = self.cfg_dic['simv'][gn]
        gg_dir = self.ced['SIMV_DIR']+os.sep+gn.strip()
        simv_cfg_json = gg_dir+os.sep+'simv_cfg.json'
        os.makedirs(gg_dir, exist_ok=True)
        ojson = {}
        if os.path.isfile(simv_cfg_json):
            with open(simv_cfg_json) as jf:
                ojson = json.load(jf)
        self.cfg_dic['simv']['DEFAULT'].update(gn_cfg)
        njson = dict(self.cfg_dic['simv']['DEFAULT'])
        if ojson != njson or self.fresh_flg:
            with open(simv_cfg_json, 'w') as jf:
                json.dump(njson, jf)
    def gen_smf_lst(self, gn):
        smf_lst = []
        for sm in self.rd_cfg('simv', gn, 'sub_modules'):
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
    def chk_simv_flist(self, gn, f_tup, tb_flg=False):
        gf_dir = self.ced['SIMV_DIR']+os.sep+gn.strip()
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
    def gen_simv_dic(self, gn):
        self.chk_simv_cfg(gn)
        simv_dic = {'name': gn.strip()}
        ca_opts_lst = self.rd_cfg('simv', gn, 'custom_ana_opts')
        ce_opts_lst = self.rd_cfg('simv', gn, 'custom_elab_opts')
        if self.regr_flg:
            ca_opts_lst = self.rd_cfg(
                'proj', 'regression_opts', 'custom_ana_opts')+ca_opts_lst
            ce_opts_lst = self.rd_cfg(
                'proj', 'regression_opts', 'custom_elab_opts')+ce_opts_lst
        cov_ce_lst = (self.rd_cfg('simv', gn, 'cov_elab_opts') if
                      self.rd_cfg('simv', gn, 'cov') == ['on'] else [])
        wf_lst = self.rd_cfg('simv', gn, 'wave_format')
        simv_dic['wave_format'] = 'fsdb' if not wf_lst else wf_lst[0]
        wave_ce_lst = (self.rd_cfg('simv', gn, 'wave_elab_opts')+
                       self.rd_cfg('simv', gn, 'wf_{0}_elab_opts'.format(
                           simv_dic['wave_format'])) if
                       self.rd_cfg('simv', gn, 'wave') == ['on'] else [])
        gui_ce_lst = (self.rd_cfg('simv', gn, 'gui_elab_opts') if
                      self.rd_cfg('simv', gn, 'gui') == ['on'] else [])
        prof_ce_lst = (self.rd_cfg('simv', gn, 'prof_elab_opts') if
                       self.rd_cfg('simv', gn, 'prof') == ['on'] else [])
        fpga_ca_lst = (self.rd_cfg('simv', gn, 'fpga_ana_opts') if
                       self.rd_cfg('simv', gn, 'fpga') == ['on'] else [])
        simv_dic['ca_opts'] = ' '.join(ca_opts_lst+fpga_ca_lst)
        simv_dic['ce_opts'] = ' '.join(
            ce_opts_lst+cov_ce_lst+wave_ce_lst+gui_ce_lst+prof_ce_lst).replace(
                '{{simv_name}}', simv_dic['name'])
        dut_flist_lst = ([self.ced['MODULE_FLIST']+os.sep+'rtl.flist'] +
                         self.gen_smf_lst(gn))
        df_tup = filelst_gen.FilelstGen(self.LOG).gen_file_lst(dut_flist_lst)
        (simv_dic['dut_dir_lst'], simv_dic['dut_file_lst'],
         simv_dic['vhdl_file_lst']) = df_tup
        self.chk_simv_flist(gn, df_tup, False)
        tb_flist_lst = [self.ced['MODULE_FLIST']+os.sep+'tb.flist']
        tf_tup = filelst_gen.FilelstGen(self.LOG).gen_file_lst(tb_flist_lst)
        simv_dic['tb_dir_lst'], simv_dic['tb_file_lst'], _ = tf_tup
        self.chk_simv_flist(gn, tf_tup, True)
        simv_dic['tb_dep_file_lst'] = self.vip_dep_file_lst + list(
            pcom.find_iter(self.ced['MODULE_TB'], '*.sv'))
        vhdl_tool_lst = self.rd_cfg('simv', gn, 'vhdl_tool')
        simv_dic['vhdl_tool'] = (
            vhdl_tool_lst[0] if vhdl_tool_lst else 'vhdlan')
        simv_dic['vhdl_da_opts'] = ' '.join(self.rd_cfg(
            'simv', gn, 'vt_{0}_dut_ana_opts'.format(simv_dic['vhdl_tool'])))
        simv_dic['vhdl_ta_opts'] = ' '.join(self.rd_cfg(
            'simv', gn, 'vt_{0}_tb_ana_opts'.format(simv_dic['vhdl_tool'])))
        ana_tool_lst = self.rd_cfg('simv', gn, 'ana_tool')
        simv_dic['ana_tool'] = ana_tool_lst[0] if ana_tool_lst else 'vlogan'
        simv_dic['da_opts'] = ' '.join(self.rd_cfg(
            'simv', gn, 'at_{0}_dut_ana_opts'.format(simv_dic['ana_tool'])))
        simv_dic['ta_opts'] = ' '.join(self.rd_cfg(
            'simv', gn, 'at_{0}_tb_ana_opts'.format(simv_dic['ana_tool'])))
        elab_tool_lst = self.rd_cfg('simv', gn, 'elab_tool')
        simv_dic['elab_tool'] = elab_tool_lst[0] if elab_tool_lst else 'vcs'
        simv_dic['e_opts'] = ' '.join(self.rd_cfg(
            'simv', gn, 'et_{0}_elab_opts'.format(simv_dic['elab_tool'])))
        simv_dic['w_opts'] = ' '.join(self.rd_cfg('simv', gn, 'verdi_opts'))
        tb_top_lst = self.rd_cfg('simv', gn, 'tb_top')
        simv_dic['tb_top'] = tb_top_lst[0] if tb_top_lst else 'test_top'
        simv_dic['pre_cmd_lst'] = [
            cc.replace('{{simv_name}}', simv_dic['name']) for cc in
            self.rd_cfg('simv', gn, 'pre_cmd') if cc]
        simv_dic['post_cmd_lst'] = [
            cc.replace('{{simv_name}}', simv_dic['name']) for cc in
            self.rd_cfg('simv', gn, 'post_cmd') if cc]
        simv_dic['file_dic'] = {}
        for sec_name, sec_cont in self.cfg_dic['simv'][gn].items():
            if not sec_name.startswith('file__'):
                continue
            simv_dic['file_dic'][sec_name[6:]] = sec_cont.replace(
                '$', '$$').replace('\\', '').split(os.linesep)
        return simv_dic
    def gen_case_dic_lst(self, cn):
        case_dic = {'name': cn.strip()}
        simv_lst = self.rd_cfg('case', cn, 'simv')
        case_dic['simv'] = (simv_lst[0] if simv_lst and simv_lst[0] in
                             self.cfg_dic['simv'] else 'DEFAULT')
        self.cvs_dic[case_dic['name']] = [case_dic['simv']]
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
        su_opts = ' '.join(su_opts_lst+cov_su_lst+wave_su_lst+wg_su_lst+
                           seed_su_lst+uvm_su_lst+gui_su_lst+prof_mem_su_lst+
                           prof_time_su_lst)
        case_dic['w_opts'] = ' '.join(self.rd_cfg(
            'simv', case_dic['simv'], 'verdi_opts'))
        case_dic['file_dic'] = {}
        for sec_name, sec_cont in self.cfg_dic['case'][cn].items():
            if not sec_name.startswith('file__'):
                continue
            case_dic['file_dic'][sec_name[6:]] = sec_cont.replace(
                '$', '$$').replace('\\', '').split(os.linesep)
        case_dic_lst = []
        regr_type_lst = self.rd_cfg('case', cn, 'regression_type')
        regr_type_lst.append('all')
        seed_set = set()
        seed_lst = self.rd_cfg('case', cn, 'seed')
        rt_lst = self.rd_cfg('case', cn, 'random_times')
        loop_times = rt_lst[0] if rt_lst and rt_lst[0].isdigit() else '1'
        for i in range(int(loop_times)):
            new_case_dic = copy.deepcopy(case_dic)
            if rt_lst:
                seed = check_seed(random.randrange(1, 999999), seed_set)
                seed_set.add(seed)
                new_case_dic['seed'] = str(seed)
            elif seed_lst:
                if seed_lst[0].isdigit():
                    new_case_dic['seed'] = seed_lst[0]
                else:
                    seed = check_seed(random.randrange(1, 999999), seed_set)
                    seed_set.add(seed)
                    new_case_dic['seed'] = str(seed)
            else:
                new_case_dic['seed'] = '1'
            new_case_dic['su_opts'] = su_opts.replace(
                '{{seed}}', new_case_dic['seed']).replace(
                    '{{case_name}}', new_case_dic['name'])
            self.cvs_dic[case_dic['name']].append(new_case_dic['seed'])
            for regr_type in regr_type_lst:
                regr_type = regr_type.lower()
                cvs_tup = (new_case_dic['name'], new_case_dic['simv'],
                           new_case_dic['seed'])
                if regr_type in self.regr_dic:
                    self.regr_dic[regr_type].append(cvs_tup)
                else:
                    self.regr_dic[regr_type] = [cvs_tup]
            if self.x86_ins_flg and (self.case_lst or self.all_case_flg):
                import ins_gen
                ins_gen.InsGen(
                    self.cfg_lst, [new_case_dic['name']],
                    seed=new_case_dic['seed'],
                    path=self.ced['PROJ_MODULE']).gen_ins()
                subprocess.run(
                    'perl {0} test_name={1} seed={2} inst_mod={3} '
                    'sfile_type={4} input={5}{6}{1}{6}{2} output='
                    '{5}{6}{1}{6}{2}'.format(
                        self.test_gen_file, new_case_dic['name'],
                        new_case_dic['seed'], '16', 'asm',
                        self.ced['MODULE_OUTPUT'], os.sep), shell=True,
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            new_case_dic['pre_cmd_lst'] = [
                cc.replace('{{seed}}', new_case_dic['seed']).replace(
                    '{{case_name}}', new_case_dic['name']) for cc in
                self.rd_cfg('case', cn, 'pre_cmd') if cc]
            new_case_dic['post_cmd_lst'] = [
                cc.replace('{{seed}}', new_case_dic['seed']).replace(
                    '{{case_name}}', new_case_dic['name']) for cc in
                self.rd_cfg('case', cn, 'post_cmd') if cc]
            case_dic_lst.append(new_case_dic)
        return case_dic_lst
    def gen_mk_dic(self):
        mk_dic = {'CED': self.ced}
        simv_dic_lst = []
        for gn in self.cfg_dic['simv']:
            if self.regr_flg:
                self.cfg_dic['simv'][gn].update(
                    self.cfg_dic['proj']['regression'])
            if self.ow_dic['ae']:
                self.cfg_dic['simv'][gn].update(self.ow_dic['ae'])
            simv_dic_lst.append(self.gen_simv_dic(gn))
        case_dic_lst = []
        for cn in self.cfg_dic['case']:
            if cn == 'DEFAULT':
                continue
            if self.regr_flg:
                self.cfg_dic['case'][cn].update(
                    self.cfg_dic['proj']['regression'])
            if self.case_lst and cn not in self.case_lst:
                continue
            self.cfg_dic['case'][cn].update(self.ow_dic['su'])
            case_dic_lst += self.gen_case_dic_lst(cn)
        mk_dic['simv_dic_lst'] = simv_dic_lst
        mk_dic['case_dic_lst'] = case_dic_lst
        mk_dic['cvs_dic'] = self.cvs_dic
        mk_dic['c_lst'] = [
            os.path.basename(os.path.splitext(cc)[0]) for cc in pcom.find_iter(
                self.ced['MODULE_C'], '*.c', cur_flg=True) if
            cc] if os.path.isdir(self.ced['MODULE_C']) else []
        mk_dic['c_opts'] = self.cc_opts if self.cc_opts else ' '.join(
            self.rd_cfg('proj', 'proj', 'c_opts'))
        return mk_dic
    def gen_makefile(self):
        mk_dic = self.gen_mk_dic()
        templateLoader = jinja2.FileSystemLoader(self.ced['PJ_TEMPLATES'])
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template('Makefile')
        template_out = template.render(mk_dic)
        os.makedirs(self.ced['MODULE_OUTPUT'], exist_ok=True)
        self.LOG.info("output dir {0} is generated".format(
            self.ced['MODULE_OUTPUT']))
        mk_file = 'Makefile'
        mk_dir = self.ced['MODULE_OUTPUT']
        with open(mk_dir+os.sep+mk_file, 'w') as f:
            f.write(template_out)
        return (mk_dir, mk_file, self.cvs_dic, self.regr_dic)
