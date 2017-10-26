"""regr views"""
import datetime as dt
import json
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.http import HttpResponse
from django.conf import settings
from .models import User, Proj, Module, RegrSimv, RegrCase, RegrSim, MpRun
from .views import gen_date_range, date_range, zone_time, update_userinfo

# Create your views here.
def gen_pr_color(prt):
    """convert passing rate to color"""
    if 0 <= prt < 5:
        cls = '#FF0000'
    elif 5 <= prt < 20:
        cls = '#FF3C3C'
    elif 20 <= prt < 40:
        cls = '#FF2A00'
    elif 40 <= prt < 60:
        cls = '#FFA500'
    elif 60 <= prt < 80:
        cls = '#AEFF00'
    elif 80 <= prt < 95:
        cls = '#04FF00'
    elif 95 <= prt <= 100:
        cls = '#00FF00'
    else:
        cls = '#FF0000'
    return cls

def gen_day_dic(day_model_dic):
    """gen sim queryset dict in day"""
    day_model_lst = []
    for day_str, model_dic in day_model_dic.items():
        for model_str, pr_num_dic in model_dic.items():
            dvs = pr_num_dic['pn']/pr_num_dic['tn'] if pr_num_dic['tn'] else 0
            prt = round(100*dvs, 2)
            model_str_pr_dic = {'pn': pr_num_dic['pn'],
                                'tn': pr_num_dic['tn'],
                                'pr': prt, 'bc': gen_pr_color(prt)}
            day_model_lst.append({'day': {
                'time': {'model': model_str, 'runt': day_str},
                'model_lst':[model_str, 'None', 'None', 'None'],
                'items': model_str_pr_dic}})
    return day_model_lst

def gen_sec_dic(sim_obj_qs, sim_fk='sim', case_flg=False):
    """gen sim queryset dict in sec"""
    model_lst = []
    day_model_dic = {}
    sim_obj_qs = sim_obj_qs.order_by('-pub_date')
    sec_date_qs = sim_obj_qs.datetimes('pub_date', 'second', 'DESC')
    for sec_obj in sec_date_qs:
        sec_str = dt.datetime.strftime(sec_obj, '%Y_%m_%d_%H_%M_%S')
        sec_obj_qs = sim_obj_qs.filter(pub_date__range=
                                       gen_date_range(sec_obj.strftime("%Y_%m_%d_%H_%M_%S")))
        if not case_flg:
            day_str = dt.datetime.strftime(sec_obj, '%Y_%m_%d')
            if day_str not in day_model_dic:
                day_model_dic[day_str] = {}
            for model, model_pr_dic in gen_model_dic(sec_obj_qs, sim_fk).items():
                model_lst.append({'sec': {
                    'time': {'model': model, 'runt': sec_str},
                    'model_lst':[model, 'None', 'None', 'None'],
                    'items': model_pr_dic}})
                if model not in day_model_dic[day_str]:
                    day_model_dic[day_str][model] = {'pn': model_pr_dic['pn'],
                                                     'tn': model_pr_dic['tn']}
                else:
                    day_model_dic[day_str][model]['pn'] += model_pr_dic['pn']
                    day_model_dic[day_str][model]['tn'] += model_pr_dic['tn']
        else:
            for sim, sim_info_dic in gen_sim_dic(sec_obj_qs).items():
                model_lst.append({'sec': {
                    'time':{'case_log':sim_info_dic['status_log'], 'runt': sec_str,
                            'rund':zone_time(sim_info_dic['end_time'])},
                    'case':{'seed':sim.seed,
                            'proj_cl':sim.proj_cl,
                            'vn':sim_info_dic['vn'],
                            'bc':sim_info_dic['bc'],
                            'casename':sim_info_dic['cn'],
                            'status':sim_info_dic['status'],
                            'simu_cpu_time':sim.simu_cpu_time,
                            'regr_type':sim_info_dic['regr_type'],
                            'error_info':sim_info_dic['error_info'],
                            'error_stage':sim_info_dic['error_stage']}}})
    return model_lst+gen_day_dic(day_model_dic)

def gen_model_dic(sim_obj_qs, sim_fk):
    """gen model dict"""
    sim_obj_qs = sim_obj_qs.order_by('case_id', 'seed', '-pub_date').distinct('case_id', 'seed')
    model_dic = {}
    if sim_fk == "proj":
        func_str = 'p_name'
    elif sim_fk == 'module':
        func_str = 'm_name'
    elif sim_fk == 'case':
        func_str = 'c_name'
    for sim_obj in sim_obj_qs:
        model_obj_name = getattr(sim_obj, func_str)
        if model_obj_name not in model_dic:
            model_dic[model_obj_name] = {'pn': 0, 'tn': 0, 'pr': 0, 'bc': gen_pr_color(0),
                                         'cl_set': set(), 'rund': sim_obj.end_date,
                                         'regr_type': sim_obj.regr_types}
        if sim_obj.end_date > model_dic[model_obj_name]['rund']:
            model_dic[model_obj_name]['rund'] = sim_obj.end_date
        if sim_obj.simu_status == 'passed':
            model_dic[model_obj_name]['pn'] += 1
        model_dic[model_obj_name]['tn'] += 1
        cl_dstr = sim_obj.proj_cl[1:]
        if cl_dstr.isdigit():
            model_dic[model_obj_name]['cl_set'].add(int(cl_dstr))
    for model_obj_name, model_pr_dic in model_dic.items():
        dvs = model_pr_dic['pn']/model_pr_dic['tn'] if model_pr_dic['tn'] else 0
        model_pr_dic['pr'] = round(100*dvs, 2)
        model_pr_dic['rund'] = zone_time(model_pr_dic['rund'])
        model_pr_dic['bc'] = gen_pr_color(model_pr_dic['pr'])
        model_pr_dic['cl_range'] = 'r{0} ~ r{1}'.format(
            max(model_pr_dic['cl_set']), min(model_pr_dic['cl_set']))
        model_pr_dic.pop('cl_set')
    return model_dic

def gen_sim_dic(sim_obj_qs):
    """gen sim dic"""
    sim_obj_qs = sim_obj_qs.order_by('case_id', 'seed', '-pub_date').distinct('case_id', 'seed')
    sim_dic = {}
    for sim_obj in sim_obj_qs:
        sim_dic[sim_obj] = {
            'cn': sim_obj.c_name,
            'vn': sim_obj.v_name,
            'regr_type': sim_obj.regr_types,
            'end_time' : sim_obj.end_date}
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

def regr_query_case_dic(request):
    """query sim information from database---API"""
    if request.method == 'GET':
        date = request.GET.get('date', '')
        proj = request.GET.get('proj', '')
        module = request.GET.get('module', '')
        days = int(request.GET.get('days', ''))
        sim_qs = RegrSim.objects.filter(
            pub_date__range=gen_date_range(date, days)).filter(
                user__name='jenkins').filter(
                    module__name=module+'___'+proj)
        case_dic = gen_model_dic(sim_qs, 'case')
    return HttpResponse(json.dumps(case_dic), content_type='application/json')

class RegrUserList(ListView):
    """Regr index"""
    template_name = 'pj_app/regr.html'
    def __init__(self):
        self.user_list = []
    def get_queryset(self):
        for user_obj in User.objects.all():
            if user_obj.asic_info.get("regr"):
                self.user_list.append(user_obj.name)
    def get_context_data(self, **kwargs):
        context = super(RegrUserList, self).get_context_data(**kwargs)
        context['user_list'] = self.user_list
        context['pj_type'] = 'Regression'
        context['user'] = settings.REGR_USER
        context['team'] = settings.REGR_TEAM
        return context

def regr_get_model(request):
    """ajax--regr query regr infromtion"""
    model_lst = []
    model = request.GET.get('model')
    user = request.GET.get('user')
    proj = request.GET.get('proj')
    module = request.GET.get('module')
    tstart = request.GET.get('tstart')
    tend = request.GET.get('tend')
    if model == 'proj':
        sim_obj_qs = RegrSim.objects.filter(user__name=user,
                                            pub_date__range=date_range(tstart, tend))
        if sim_obj_qs.exists():
            model_lst = gen_sec_dic(sim_obj_qs, 'proj')
        else:
            model_lst = [{'day': {
                'time': {'model': 'None', 'runt': 'None'},
                'model_lst':['None', 'None', 'None', 'None'],
                'items': {'pn': 0, 'tn': 0, 'pr': 0, 'bc': '#fff'}}},
                         {'sec': {
                             'time': {'model': 'None', 'runt': 'None'},
                             'model_lst':['None', 'None', 'None', 'None'],
                             'items': {'pn': 0, 'tn': 0, 'pr': 0, 'bc': '#fff'}}}]
    elif model == 'module':
        sim_obj_qs = RegrSim.objects.filter(user__name=user,
                                            proj__name=proj,
                                            pub_date__range=date_range(tstart, tend))
        if sim_obj_qs.exists():
            model_lst = gen_sec_dic(sim_obj_qs, 'module')
        else:
            model_lst = [{'day': {
                'time': {'model': 'None', 'runt': 'None'},
                'model_lst':['None', 'None', 'None', 'None'],
                'items': {'pn': 0, 'tn': 0, 'pr': 0, 'bc': '#fff'}}},
                         {'sec': {
                             'time': {'model': 'None', 'runt': 'None'},
                             'model_lst':['None', 'None', 'None', 'None'],
                             'items': {'pn': 0, 'tn': 0, 'pr': 0,
                                       'bc': '#fff', 'rund':'None'}}}]
    elif model == 'case':
        sim_obj_qs = RegrSim.objects.filter(user__name=user,
                                            proj__name=proj,
                                            module__name=module+'___'+proj,
                                            pub_date__range=date_range(tstart, tend))
        if sim_obj_qs.exists():
            model_lst = gen_sec_dic(sim_obj_qs, case_flg=True)
        else:
            model_lst = [{"sec":{
                'time':{'case_log':'None', 'runt': 'None', 'rund': 'None'},
                'case':{'casename':'None', 'regr_type':'None', 'vn':'None',
                        'proj_cl':'None', 'seed':'None', 'status':'None',
                        'error_stage': 'None', 'error_info':'None',
                        'simu_cpu_time':'None', 'bc':0}}}]
    return HttpResponse(json.dumps(model_lst), content_type='application/json')

@csrf_exempt
def regr_query_insert_case(request):
    """push data to database ----API"""
    if request.method == 'POST':
        case_dic = json.loads(request.body.decode())
        user_obj, _ = User.objects.update_or_create(name=case_dic['user_name'])
        update_userinfo('regr', user_obj, case_dic['proj_name'], case_dic['m_name'])
        proj_obj, _ = Proj.objects.update_or_create(name=case_dic['proj_name'])
        module_obj, _ = Module.objects.update_or_create(name=case_dic['module_name'])
        RegrSimv.objects.update_or_create(name=case_dic['simv_name'])
        RegrCase.objects.update_or_create(name=case_dic['case_name'])
        case_date = pytz.timezone(settings.TIME_ZONE).localize(
            dt.datetime.fromtimestamp(case_dic['pub_date']))
        RegrSim.objects.create(
            pub_date=case_date,
            end_date=pytz.timezone(settings.TIME_ZONE).localize(
                dt.datetime.fromtimestamp(case_dic['end_date'])),
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
            regr_types=case_dic['regr_types'],
            case=RegrCase.objects.get(name=case_dic['case_name']),
            c_name=case_dic['c_name'],
            simv=RegrSimv.objects.get(name=case_dic['simv_name']),
            v_name=case_dic['v_name'],
            module=Module.objects.get(name=case_dic['module_name']),
            m_name=case_dic['m_name'],
            proj=Proj.objects.get(name=case_dic['proj_name']),
            p_name=case_dic['proj_name'],
            user=User.objects.get(name=case_dic['user_name']))
        mprun_qs = MpRun.objects.filter(
            user=user_obj,
            proj=proj_obj,
            module=module_obj,
            p_name=case_dic['proj_name'],
            m_name=case_dic['m_name'],
            run_time=case_date,
            pj_props=case_dic['pj_props'])
        if mprun_qs:
            for mprun_obj in mprun_qs:
                if mprun_obj.misc["status"] == "Running":
                    mprun_obj.misc["status"] = "Fault"
                    mprun_obj.save()
    return HttpResponse(json.dumps({}), content_type='application/json')
