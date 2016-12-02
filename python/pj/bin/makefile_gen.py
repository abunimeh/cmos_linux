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
        self.cgs_dic = {}
        self.regr_dic = {}
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
    def chk_group_cfg(self, gn):
        gn_cfg = self.cfg_dic['group'][gn]
        gg_dir = self.ced['GROUP_DIR']+os.sep+gn.strip()
        group_cfg_json = gg_dir+os.sep+'group_cfg.json'
        os.makedirs(gg_dir, exist_ok=True)
        ojson = {}
        if os.path.isfile(group_cfg_json):
            with open(group_cfg_json) as jf:
                ojson = json.load(jf)
        self.cfg_dic['group']['DEFAULT'].update(gn_cfg)
        njson = dict(self.cfg_dic['group']['DEFAULT'])
        if ojson != njson or self.fresh_flg:
            with open(group_cfg_json, 'w') as jf:
                json.dump(njson, jf)
    def gen_smf_lst(self, gn):
        smf_lst = []
        for sm in self.rd_cfg('group', gn, 'sub_modules'):
            if not ':' in sm:
                raise Exception(
                    "sub_modules {0} in module {1} group cfg has incorrect "
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
    def chk_group_flist(self, gn, f_tup, tb_flg=False):
        gf_dir = self.ced['GROUP_DIR']+os.sep+gn.strip()
        fn_str = 'group_tbfl.pcl' if tb_flg else 'group_dutfl.pcl'
        group_flist_pcl = gf_dir+os.sep+fn_str
        os.makedirs(gf_dir, exist_ok=True)
        opcl = ()
        if os.path.isfile(group_flist_pcl):
            with open(group_flist_pcl, 'rb') as pf:
                opcl = pickle.load(pf)
        npcl = f_tup
        if opcl != npcl:
            with open(group_flist_pcl, 'wb') as pf:
                pickle.dump(npcl, pf)
    def gen_group_dic(self, gn):
        self.chk_group_cfg(gn)
        group_dic = {'name': gn.strip()}
        ca_opts_lst = self.rd_cfg('group', gn, 'custom_ana_opts')
        ce_opts_lst = self.rd_cfg('group', gn, 'custom_elab_opts')
        if self.regr_flg:
            ca_opts_lst = self.rd_cfg(
                'proj', 'regression_opts', 'custom_ana_opts')+ca_opts_lst
            ce_opts_lst = self.rd_cfg(
                'proj', 'regression_opts', 'custom_elab_opts')+ce_opts_lst
        cov_ce_lst = (self.rd_cfg('group', gn, 'cov_elab_opts') if
                      self.rd_cfg('group', gn, 'cov') == ['on'] else [])
        wf_lst = self.rd_cfg('group', gn, 'wave_format')
        group_dic['wave_format'] = 'fsdb' if not wf_lst else wf_lst[0]
        wave_ce_lst = (self.rd_cfg('group', gn, 'wave_elab_opts')+
                       self.rd_cfg('group', gn, 'wf_{0}_elab_opts'.format(
                           group_dic['wave_format'])) if
                       self.rd_cfg('group', gn, 'wave') == ['on'] else [])
        gui_ce_lst = (self.rd_cfg('group', gn, 'gui_elab_opts') if
                      self.rd_cfg('group', gn, 'gui') == ['on'] else [])
        prof_ce_lst = (self.rd_cfg('group', gn, 'prof_elab_opts') if
                       self.rd_cfg('group', gn, 'prof') == ['on'] else [])
        fpga_ca_lst = (self.rd_cfg('group', gn, 'fpga_ana_opts') if
                       self.rd_cfg('group', gn, 'fpga') == ['on'] else [])
        group_dic['ca_opts'] = ' '.join(ca_opts_lst+fpga_ca_lst)
        group_dic['ce_opts'] = ' '.join(
            ce_opts_lst+cov_ce_lst+wave_ce_lst+gui_ce_lst+prof_ce_lst).replace(
                '{{group_name}}', group_dic['name'])
        dut_flist_lst = ([self.ced['MODULE_FLIST']+os.sep+'rtl.flist'] +
                         self.gen_smf_lst(gn))
        df_tup = filelst_gen.FilelstGen(self.LOG).gen_file_lst(dut_flist_lst)
        (group_dic['dut_dir_lst'], group_dic['dut_file_lst'],
         group_dic['vhdl_file_lst']) = df_tup
        self.chk_group_flist(gn, df_tup, False)
        tb_flist_lst = [self.ced['MODULE_FLIST']+os.sep+'tb.flist']
        tf_tup = filelst_gen.FilelstGen(self.LOG).gen_file_lst(tb_flist_lst)
        group_dic['tb_dir_lst'], group_dic['tb_file_lst'], _ = tf_tup
        self.chk_group_flist(gn, tf_tup, True)
        group_dic['tb_dep_file_lst'] = self.vip_dep_file_lst + list(
            pcom.find_iter(self.ced['MODULE_TB'], '*.sv'))
        vhdl_tool_lst = self.rd_cfg('group', gn, 'vhdl_tool')
        group_dic['vhdl_tool'] = (
            vhdl_tool_lst[0] if vhdl_tool_lst else 'vhdlan')
        group_dic['vhdl_da_opts'] = ' '.join(self.rd_cfg(
            'group', gn, 'vt_{0}_dut_ana_opts'.format(group_dic['vhdl_tool'])))
        group_dic['vhdl_ta_opts'] = ' '.join(self.rd_cfg(
            'group', gn, 'vt_{0}_tb_ana_opts'.format(group_dic['vhdl_tool'])))
        ana_tool_lst = self.rd_cfg('group', gn, 'ana_tool')
        group_dic['ana_tool'] = ana_tool_lst[0] if ana_tool_lst else 'vlogan'
        group_dic['da_opts'] = ' '.join(self.rd_cfg(
            'group', gn, 'at_{0}_dut_ana_opts'.format(group_dic['ana_tool'])))
        group_dic['ta_opts'] = ' '.join(self.rd_cfg(
            'group', gn, 'at_{0}_tb_ana_opts'.format(group_dic['ana_tool'])))
        elab_tool_lst = self.rd_cfg('group', gn, 'elab_tool')
        group_dic['elab_tool'] = elab_tool_lst[0] if elab_tool_lst else 'vcs'
        group_dic['e_opts'] = ' '.join(self.rd_cfg(
            'group', gn, 'et_{0}_elab_opts'.format(group_dic['elab_tool'])))
        group_dic['w_opts'] = ' '.join(self.rd_cfg('group', gn, 'verdi_opts'))
        tb_top_lst = self.rd_cfg('group', gn, 'tb_top')
        group_dic['tb_top'] = tb_top_lst[0] if tb_top_lst else 'test_top'
        group_dic['pre_cmd_lst'] = [
            cc.replace('{{group_name}}', group_dic['name']) for cc in
            self.rd_cfg('group', gn, 'pre_cmd') if cc]
        group_dic['post_cmd_lst'] = [
            cc.replace('{{group_name}}', group_dic['name']) for cc in
            self.rd_cfg('group', gn, 'post_cmd') if cc]
        group_dic['file_dic'] = {}
        for sec_name, sec_cont in self.cfg_dic['group'][gn].items():
            if not sec_name.startswith('file__'):
                continue
            group_dic['file_dic'][sec_name[6:]] = sec_cont.replace(
                '$', '$$').replace('\\', '').split(os.linesep)
        return group_dic
    def gen_case_dic_lst(self, cn):
        case_dic = {'name': cn.strip()}
        group_lst = self.rd_cfg('case', cn, 'group')
        case_dic['group'] = (group_lst[0] if group_lst and group_lst[0] in
                             self.cfg_dic['group'] else 'DEFAULT')
        self.cgs_dic[case_dic['name']] = [case_dic['group']]
        tb_top_lst = self.rd_cfg('group', case_dic['group'], 'tb_top')
        case_dic['tb_top'] = tb_top_lst[0] if tb_top_lst else 'test_top'
        case_dic['wave'] = True if self.rd_cfg(
            'case', cn, 'wave') == ['on'] else False
        wf_lst = self.rd_cfg('group', case_dic['group'], 'wave_format')
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
            'group', case_dic['group'], 'verdi_opts'))
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
            self.cgs_dic[case_dic['name']].append(new_case_dic['seed'])
            for regr_type in regr_type_lst:
                regr_type = regr_type.lower()
                ngs_tup = (new_case_dic['name'], new_case_dic['group'],
                           new_case_dic['seed'])
                if regr_type in self.regr_dic:
                    self.regr_dic[regr_type].append(ngs_tup)
                else:
                    self.regr_dic[regr_type] = [ngs_tup]
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
        group_dic_lst = []
        for gn in self.cfg_dic['group']:
            if self.regr_flg:
                self.cfg_dic['group'][gn].update(
                    self.cfg_dic['proj']['regression'])
            if self.ow_dic['ae']:
                self.cfg_dic['group'][gn].update(self.ow_dic['ae'])
            group_dic_lst.append(self.gen_group_dic(gn))
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
        mk_dic['group_dic_lst'] = group_dic_lst
        mk_dic['case_dic_lst'] = case_dic_lst
        mk_dic['cgs_dic'] = self.cgs_dic
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
        return (mk_dir, mk_file, self.cgs_dic, self.regr_dic)
