from .models import User, Proj, Module, Simv, Case, Sim
from django.views.generic import ListView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import collections
import json
import pytz
import ldap3
import datetime as dt
import copy

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

import matplotlib.pyplot as plt
import numpy as np

# Create your views here.

def ldap3_query():
    s = ldap3.Server('ldap://172.51.13.98:1389',get_info=ldap3.ALL)
    userdn = 'uid='+'chenh'+',ou=People,dc=sari,dc=com'
    c_ins = ldap3.Connection(s,user=userdn,password="nfs123")
    c_ins.bind()
    c_ins.search("ou=Group,dc=sari,dc=com",'(objectclass=posixGroup)',attributes=ldap3.ALL_ATTRIBUTES)
    g_entries = c_ins.entries
    g_entries.sort()
    c_ins.search("ou=People,dc=sari,dc=com",'(objectclass=person)',attributes=ldap3.ALL_ATTRIBUTES)    
    p_entries = c_ins.entries
    p_entries.sort()
    model_dic = collections.OrderedDict()
    team_dic = collections.OrderedDict()
    for pp_entry in p_entries:
        if pp_entry.entry_attributes_as_dict.get('userPKCS12',False) and (pp_entry.entry_attributes_as_dict.get('userPKCS12')[0] == b'0'):
            if pp_entry.gidNumber.value not in model_dic:
                model_dic[pp_entry.gidNumber.value]=[]
                model_dic[pp_entry.gidNumber.value].append(pp_entry.uid.value)
            else:
                model_dic[pp_entry.gidNumber.value].append(pp_entry.uid.value)
    for gp_entry in g_entries:
        if gp_entry.entry_attributes_as_dict.get('description','none') != 'none':
            team_dic[gp_entry.cn.value] = model_dic[gp_entry.gidNumber.value]
    return team_dic

def sql_query():
    user_dic = collections.OrderedDict()
    for user_obj in User.objects.all().order_by('name'):
        proj_list = []
        for proj_obj in Sim.objects.filter(user__name = user_obj.name).distinct('proj'):
            module_list = []
            for module_obj in Sim.objects.filter(user__name = user_obj.name).filter(proj__name=proj_obj.proj.name).distinct('module'):
                module_list.append({"n":module_obj.module.mname()})
            proj_list.append({"n":proj_obj.proj.name , "s":module_list})
        user_dic[user_obj.name] = proj_list
    return user_dic

def query_select(request):
    query_list = []
    sql_dic = sql_query()
    for tm_key, tm_value in ldap3_query().items():
        user_list = []
        for user_nm in tm_value:
            if user_nm in sql_dic:
                user_list.append({"n":user_nm, "s":sql_dic[user_nm]})
            else:
                user_list.append({"n":user_nm, "s":[{'n': 'None', 's':[{'n': 'None'}]}]})
        team_dic={"n": tm_key, "s": user_list}
        query_list.append(team_dic)
    return HttpResponse(json.dumps(query_list), content_type='application/json')

def gen_date_range(date_str, diff=1):
    diff = int(diff)
    tz = pytz.timezone(settings.TIME_ZONE)
    if len(date_str) == 10:
        et = dt.datetime.strptime(
            date_str, '%Y_%m_%d')+dt.timedelta(days=1)
        bt = et-dt.timedelta(days=diff)
    else:
        et = dt.datetime.strptime(
            date_str, '%Y_%m_%d_%H_%M_%S')+dt.timedelta(seconds=1)
        bt = et-dt.timedelta(seconds=diff)
    bt = tz.localize(bt)
    et = tz.localize(et)
    return (bt, et)

def date_range(tstart, tend):   
    tz = pytz.timezone(settings.TIME_ZONE)
    bt = dt.datetime.strptime(tstart, '%Y-%m-%d')
    et = dt.datetime.strptime(tend, '%Y-%m-%d') + dt.timedelta(days=1)
    bt = tz.localize(bt)
    et = tz.localize(et)
    return (bt, et)

def gen_pr_color(pr):
    if 0<=pr<5:
        cs = '#FF0000'
    elif 5<=pr<20:
        cs = '#FF3C3C'
    elif 20<=pr<40:
        cs = '#FF2A00'
    elif 40<=pr<60:
        cs = '#FFA500'
    elif 60<=pr<80:
        cs = '#AEFF00'
    elif 80<=pr<95:
        cs = '#04FF00'
    elif 95<=pr<=100:
        cs = '#00FF00'
    else:
        cs = '#FF0000'
    return cs

def gen_wrap_dic(sim_obj_qs, sim_fk='sim', sec_flg=False ,day_flg=False):
    model_list = []
    model_dic = collections.OrderedDict()
    sim_obj_qs = sim_obj_qs.order_by('-pub_date')
    if day_flg:
        day_date_qs = sim_obj_qs.distinct('pub_date').datetimes('pub_date', 'day','DESC')
        for day_obj in day_date_qs:
            day_str = dt.datetime.strftime(day_obj, '%Y_%m_%d')
            day_obj_qs = sim_obj_qs.filter(pub_date__range=gen_date_range(day_obj.strftime("%Y_%m_%d")))
            for model, model_pr_dic in gen_model_dic(day_obj_qs, sim_fk).items():
                model_list.append({'day': {'time': {'model': model, 'runt': day_str}, 'model_list':[model,'None','None','None'] , 'items': model_pr_dic}})
    else:
        sec_date_qs = sim_obj_qs.distinct('pub_date').datetimes('pub_date', 'second','DESC')
        for sec_obj in sec_date_qs:
            sec_str = dt.datetime.strftime(sec_obj, '%Y_%m_%d_%H_%M_%S')
            sec_obj_qs = sim_obj_qs.filter(pub_date__range=gen_date_range(sec_obj.strftime("%Y_%m_%d_%H_%M_%S")))
            if not sec_flg:
                for model, model_pr_dic in gen_model_dic(sec_obj_qs, sim_fk).items():
                    model_list.append({'sec': {'time': {'model': model, 'runt': sec_str}, 'model_list':[model,'None','None','None'] , 'items': model_pr_dic}})
            else:
                for sim, sim_info_dic in gen_sim_dic(sec_obj_qs).items():
                    model_list.append({'sec': {'time': {'case_log':sim_info_dic['status_log'], 'runt': sec_str}, 'case':{'casename':sim.case.cname(), 'vn':sim.case.vname(), 'proj_cl':sim.proj_cl, 'seed':sim.seed, 'status':sim_info_dic['status'],  'error_stage':sim_info_dic['error_stage'], 'error_info': sim_info_dic['error_info'], 'simu_cpu_time':sim.simu_cpu_time,'bc': sim_info_dic['bc']}}})
    return  model_list


def gen_model_dic(sim_obj_qs, sim_fk): 
    sim_obj_qs = sim_obj_qs.order_by('case_id', 'seed', '-pub_date').distinct('case_id', 'seed')
    model_dic = {}
    if sim_fk == "proj":
        func_str = 'pname'
    elif sim_fk == 'module':
        func_str = 'mname'
    elif sim_fk == 'case':
        func_str = 'cname'
    for sim_obj in sim_obj_qs:
        model_obj_name = getattr(getattr(sim_obj, sim_fk.lower()), func_str)()
        if model_obj_name not in model_dic:
            model_dic[model_obj_name] = {'pn': 0, 'tn': 0, 'pr': 0, 'bc': gen_pr_color(0), 'cl_set': set()}
        if sim_obj.simu_status == 'passed':
            model_dic[model_obj_name]['pn'] += 1
        model_dic[model_obj_name]['tn'] += 1
        cl_dstr = sim_obj.proj_cl[1:]
        if cl_dstr.isdigit():
            model_dic[model_obj_name]['cl_set'].add(int(cl_dstr))
    for model_obj_name, model_pr_dic in model_dic.items():
        dv = model_pr_dic['pn']/model_pr_dic['tn'] if model_pr_dic['tn'] else 0
        model_pr_dic['pr'] = round(100*dv, 2)
        model_pr_dic['bc'] = gen_pr_color(model_pr_dic['pr'])
        model_pr_dic['cl_range'] = 'r{0} ~ r{1}'.format(
            max(model_pr_dic['cl_set']), min(model_pr_dic['cl_set']))
        model_pr_dic.pop('cl_set')
    return model_dic

def gen_sim_dic(sim_obj_qs):
    sim_obj_qs = sim_obj_qs.order_by('case_id', 'seed', '-pub_date').distinct('case_id', 'seed')
    sim_dic = {}
    for sim_obj in sim_obj_qs:
        sim_dic[sim_obj] = {
            'cn': sim_obj.case.cname(),
            'vn': sim_obj.simv.vname()}
        if (sim_obj.simu_status == 'passed' and
            sim_obj.elab_status == 'passed' and
            sim_obj.tb_ana_status == 'passed' and
            sim_obj.dut_ana_status == 'passed'):
            sim_dic[sim_obj]['status'] = sim_obj.simu_status
            sim_dic[sim_obj]['bc'] = '#00FF2A'
            sim_dic[sim_obj]['error_stage'] = 'NA'
            sim_dic[sim_obj]['error_info'] = sim_obj.simu_error
            sim_dic[sim_obj]['status_log'] = sim_obj.simu_log
        elif sim_obj.elab_status == 'passed':
            sim_dic[sim_obj]['status'] = sim_obj.simu_status
            sim_dic[sim_obj]['bc'] = '#FF2A00'
            sim_dic[sim_obj]['error_stage'] = 'simulation'
            sim_dic[sim_obj]['error_info'] = sim_obj.simu_error
            sim_dic[sim_obj]['status_log'] = sim_obj.simu_log
        elif sim_obj.tb_ana_status == 'passed':
            sim_dic[sim_obj]['status'] = sim_obj.elab_status
            sim_dic[sim_obj]['bc'] = '#FF2A00'
            sim_dic[sim_obj]['error_stage'] = 'elaboration'
            sim_dic[sim_obj]['error_info'] = sim_obj.elab_error
            sim_dic[sim_obj]['status_log'] = sim_obj.elab_log
        elif sim_obj.dut_ana_status == 'passed':
            sim_dic[sim_obj]['status'] = sim_obj.tb_ana_status
            sim_dic[sim_obj]['bc'] = '#FF2A00'
            sim_dic[sim_obj]['error_stage'] = 'tb analysis'
            sim_dic[sim_obj]['error_info'] = sim_obj.tb_ana_error
            sim_dic[sim_obj]['status_log'] = sim_obj.tb_ana_log
        else:
            sim_dic[sim_obj]['status'] = sim_obj.dut_ana_status
            sim_dic[sim_obj]['bc'] = '#FF2A00'
            sim_dic[sim_obj]['error_stage'] = 'dut analysis'
            sim_dic[sim_obj]['error_info'] = sim_obj.dut_ana_error
            sim_dic[sim_obj]['status_log'] = sim_obj.dut_ana_log
    return sim_dic

def query_case_dic(request):
    if request.method == 'GET':
        date = request.GET.get('date', '')
        proj = request.GET.get('proj', '')
        module = request.GET.get('module', '')
        days = int(request.GET.get('days', ''))
        sim_qs = Sim.objects.filter(
            pub_date__range=gen_date_range(date, days)).filter(
                user__name='jenkins').filter(
                    module__name=module+'___'+proj)
        case_dic = gen_model_dic(sim_qs, 'case')
    return HttpResponse(json.dumps(case_dic), content_type='application/json')

@csrf_exempt
def query_insert_case(request):
    if request.method == 'POST':
        case_dic = json.loads(request.body.decode())
        User.objects.update_or_create(name=case_dic['user_name'])
        Proj.objects.update_or_create(name=case_dic['proj_name'])
        Module.objects.update_or_create(name=case_dic['module_name'])
        Simv.objects.update_or_create(name=case_dic['simv_name'])
        Case.objects.update_or_create(name=case_dic['case_name'])
        Sim.objects.create(
            pub_date=pytz.timezone(settings.TIME_ZONE).localize(
                dt.datetime.fromtimestamp(case_dic['pub_date'])),
            proj_cl=case_dic['proj_cl'], seed=case_dic['seed'],
            dut_ana_log=case_dic['dut_ana_log'],
            dut_ana_status=case_dic['dut_ana_status'],
            dut_ana_error=case_dic['dut_ana_error'],
            tb_ana_log=case_dic['tb_ana_log'],
            tb_ana_status=case_dic['tb_ana_status'],
            tb_ana_error=case_dic['tb_ana_error'],
            elab_log=case_dic['elab_log'],
            elab_status=case_dic['elab_status'],
            elab_error=case_dic['elab_error'],
            simu_log=case_dic['simu_log'],
            simu_status=case_dic['simu_status'],
            simu_error=case_dic['simu_error'],
            comp_cpu_time=case_dic['comp_cpu_time'],
            simu_cpu_time=case_dic['simu_cpu_time'],
            simu_time=case_dic['simu_time'],
            case=Case.objects.get(name=case_dic['case_name']),
            simv=Simv.objects.get(name=case_dic['simv_name']),
            module=Module.objects.get(name=case_dic['module_name']),
            proj=Proj.objects.get(name=case_dic['proj_name']),
            user=User.objects.get(name=case_dic['user_name']))
    return HttpResponse(json.dumps({}), content_type='application/json')

class UserList(ListView):
    template_name = 'regr/regr.html'
    def get_queryset(self):
        user_list = []
        for user_obj in User.objects.all().order_by('name'):
            user_list.append(user_obj.name)
        self.user_list = user_list
    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['user_list'] = self.user_list
        return context

def get_model(request):
    model_dic = collections.OrderedDict()
    model = request.GET.get('model')
    user = request.GET.get('user')
    proj = request.GET.get('proj')
    module = request.GET.get('module')
    tstart = request.GET.get('tstart')
    tend = request.GET.get('tend')
    time_flag = request.GET.get('tflag')
    if model == 'proj':
        if time_flag == 'day':
            sim_obj_qs = Sim.objects.filter(user__name=user).filter(pub_date__range=date_range(tstart,tend))
            if sim_obj_qs.count()==0:
                model_dic['data']= [{'day': {'time': {'model': 'None', 'runt': 'None'}, 'model_list':['None','None','None','None'] , 'items': {'pn': 0, 'tn': 0, 'pr': 0, 'bc': '#fff' }}}]
            else:
                model_dic['data'] = gen_wrap_dic(sim_obj_qs, 'proj', day_flg= True)
        elif time_flag == 'sec':
            sim_obj_qs = Sim.objects.filter(user__name=user).filter(pub_date__range=date_range(tstart,tend))
            if sim_obj_qs.count()==0:
                model_dic['data']= [{'sec': {'time': {'model': 'None', 'runt': 'None'}, 'model_list':['None','None','None','None'] , 'items': {'pn': 0, 'tn': 0, 'pr': 0, 'bc': '#fff' }}}]
            else:
                model_dic['data'] = gen_wrap_dic(sim_obj_qs, 'proj')
    elif model == 'module':
        if time_flag == 'day':
            sim_obj_qs = Sim.objects.filter(user__name=user).filter(proj__name=proj).filter(pub_date__range=date_range(tstart,tend))
            if sim_obj_qs.count()==0:
                model_dic['data']= [{'day': {'time': {'model': 'None', 'runt': 'None'}, 'model_list':['None','None','None','None'] , 'items': {'pn': 0, 'tn': 0, 'pr': 0, 'bc': '#fff' }}}]
            else:
                model_dic['data']= gen_wrap_dic(sim_obj_qs, 'module', day_flg= True)
        elif time_flag == 'sec':
            sim_obj_qs = Sim.objects.filter(user__name=user).filter(proj__name=proj).filter(pub_date__range=date_range(tstart,tend))
            if sim_obj_qs.count()==0:
                model_dic['data']= [{'sec': {'time': {'model': 'None', 'runt': 'None'}, 'model_list':['None','None','None','None'] , 'items': {'pn': 0, 'tn': 0, 'pr': 0, 'bc': '#fff' }}}]
            else:
                model_dic['data'] = gen_wrap_dic(sim_obj_qs, 'module')
    elif model == 'case':
        sim_obj_qs = Sim.objects.filter(user__name=user).filter(proj__name=proj).filter(module__name=module+'___'+proj).filter(pub_date__range=date_range(tstart,tend))
        if sim_obj_qs.count()==0:
            model_dic['data']=[{"sec":{'time':{'case_log':'None', 'runt': 'None'}, 'case':{'casename':'None' ,'vn':'None', 'proj_cl':'None', 'seed':'None', 'status':'None', 'error_stage': 'None','error_info':'None', 'simu_cpu_time':'None','bc':0}}}]
        else:
            model_dic['data'] = gen_wrap_dic(sim_obj_qs,  sec_flg=True)
    return HttpResponse(json.dumps(model_dic),content_type='application/json')
