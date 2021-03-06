"""dc views """
import datetime as dt
import collections
from collections import OrderedDict as od_dict
import os
import json
from nested_dict import nested_dict
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import User, Proj, Module, DcRun
from .views import gen_date_range, date_range, zone_time, update_userinfo

def gen_slack_interv(slk_lst):
    """slack values range list"""
    slk_num_lst = [0]*5
    if slk_lst:
        for slk in slk_lst:
            slk = slk*(-1000)
            if slk < 100:
                slk_num_lst[0] += 1
            elif 100 <= slk < 300:
                slk_num_lst[1] += 1
            elif 300 <= slk < 500:
                slk_num_lst[2] += 1
            elif 500 <= slk < 1000:
                slk_num_lst[3] += 1
            else:
                slk_num_lst[4] += 1
    return slk_num_lst

def gen_tm_dic(lv_dic):
    """statistics group path numbers"""
    gp_num_dic = collections.defaultdict(int)
    if lv_dic:
        for gse, slk_lst in lv_dic.items():
            slk_len = len(slk_lst)
            lv_dic[gse] = {'slk_num':gen_slack_interv(slk_lst),
                           'gse_sum': slk_len}
            gp_num_dic[gse.split('**')[0]] += slk_len
        lv_dic['gp'] = od_dict(gp_num_dic)
    return dict(lv_dic)

def dict_deal_key(key_dic, val_dic, merg_dic):
    """deal dict key format"""
    for gpk, gpv in key_dic.items():
        if gpk in ("Cell Count", "Area", "qor_pw_rpt", "Power"):
            merg_dic[gpk.replace(" ", "_").lower()] = {
                "items": val_dic[gpk], "values": gpv}
        else:
            merg_dic['tpg_items'] = val_dic[gpk]
            merg_dic['tpg'][gpk] = gpv
    return merg_dic

def merger_dic(dic1, dic2=None):
    """Merger the same keys of two dict"""
    key_dic = collections.defaultdict(list)
    val_dic = collections.defaultdict(list)
    merg_dic = collections.defaultdict(dict)
    if dic2:
        for gpk, gpv in dic1.items():
            if gpk not in dic2:
                continue
            if gpk == "qor_pw_rpt":
                merg_dic[gpk] = {'ref': dict(gpv),
                                 'tar': dict(dic2[gpk])}
            else:
                for gpkk, gpvv in gpv.items():
                    key_dic[gpk].append(gpvv)
                    key_dic[gpk].append(dic2[gpk].get(gpkk, "NA"))
                    val_dic[gpk].append(gpkk)
    else:
        for gpk, gpv in dic1.items():
            if gpk == "qor_pw_rpt":
                merg_dic[gpk] = {'ref': dict(gpv)}
            else:
                for gpkk, gpvv in gpv.items():
                    key_dic[gpk].append(gpvv)
                    val_dic[gpk].append(gpkk)
    return dict(dict_deal_key(key_dic, val_dic, merg_dic))

def gen_qor_dic(rpt_qs, ref_tm, tar_tm):
    """gen qor report key parameters dic """
    ref_dic = query_rpt_qs(rpt_qs, ref_tm)
    if not ref_dic:
        return {"ref_qor_null": True,
                "ref_tm": ref_tm}
    if tar_tm != 'no_tm':
        tar_dic = query_rpt_qs(rpt_qs, tar_tm)
        if not tar_dic:
            return {"tar_qor_null": True,
                    "tar_tm": tar_tm}
        qor_dic = merger_dic(ref_dic, tar_dic)
    else:
        qor_dic = merger_dic(ref_dic)
    if qor_dic:
        return qor_dic

def query_tm_lvl(rpt_qs, ref_tm, lvl='Level 1'):
    """choose different levels to show startpoint to
    endpoint numbers in differe intervals"""
    lv_dic = collections.defaultdict(list)
    nlv_dic = collections.defaultdict(list)
    tm_dic = query_time_qs(rpt_qs, ref_tm)
    for tm_k, tm_val in tm_dic.items():
        if tm_val and tm_k not in ('gp_sum', 'log_path'):
            for tm_lst in tm_val:
                if 'in2' in tm_k  or '2out' in tm_k:
                    tm_key = (tm_k+'**'+tm_lst[0]+'**'+tm_lst[1])
                    nlv_dic[tm_key].append(tm_lst[2])
                else:
                    st_pit_lst = tm_lst[0].split('/')
                    ed_pit_lst = tm_lst[1].split('/')
                    lvn = int(lvl.split(" ")[1])
                    tm_key = (tm_k+'**'+os.path.join(*st_pit_lst[0:lvn])
                              + '**' + os.path.join(*ed_pit_lst[0:lvn]))
                    lv_dic[tm_key].append(tm_lst[2])
    rpt_dic = {'nlv_gp': gen_tm_dic(nlv_dic), 'lv_gp': gen_tm_dic(lv_dic),
               'gp_sum': tm_dic['gp_sum'], 'log_path': tm_dic['log_path']}
    return rpt_dic

def query_time_qs(rpt_qs, run_tm):
    """dc time report queryset interface"""
    rpt_dic = collections.defaultdict(list)
    dcrun_qs = rpt_qs.filter(run_time__range=gen_date_range(run_tm))
    tmrpt_dic = dcrun_qs.first().time_rpt
    if tmrpt_dic:
        gp_sum = 0
        for se_dic in tmrpt_dic["timing"]:
            rpt_dic[se_dic["Path Group"]].append([se_dic["Startpoint"],
                                                  se_dic["Endpoint"],
                                                  se_dic["slack"]])
            gp_sum += 1
        rpt_dic['gp_sum'] = gp_sum
        rpt_dic["log_path"] = tmrpt_dic["log_path"]
    return rpt_dic

def query_rpt_qs(rpt_qs, run_tm):
    """dc qor and power reports queryset interface"""
    rpt_dic = collections.defaultdict(dict)
    dcrun_qs = rpt_qs.filter(run_time__range=gen_date_range(run_tm))
    qorpt_dic = dcrun_qs.first().qor_rpt
    if qorpt_dic:
        rpt_dic['qor_pw_rpt'] = od_dict({'run_time': run_tm,
                                         'qor_log': qorpt_dic["log_path"]})
        for qor_type, qor_dic in qorpt_dic.items():
            if qor_type in ("log_path",
                            "Design Rules",
                            "Compile CPU Statistics"):
                continue
            if qor_type not in ("Area", "Cell Count"):
                qor_dic = {type_nm: qor_dic[type_nm] for type_nm in qor_dic.keys() -
                           {"Worst Hold Violation",
                            "Total Hold Violation",
                            "No. of Hold Violations"}}
                qor_dic = od_dict(qor_dic)
            rpt_dic[qor_type] = qor_dic
        for qor, qor_dic in rpt_dic.items():
            if (qor not in ('Cell Count', 'Area', 'qor_pw_rpt') and
                    qor_dic.get("Critical Path Clk Period", None)):
                qor_dic.move_to_end("Critical Path Clk Period")
            rpt_dic[qor] = od_dict(reversed(list(qor_dic.items())))
    pwrpt_dic = dcrun_qs.first().power_rpt
    if pwrpt_dic:
        rpt_dic['qor_pw_rpt']['pw_log'] = pwrpt_dic["log_path"]
        rpt_dic['Power'] = od_dict({"Internal": pwrpt_dic["internal_pw"],
                                    "Switching": pwrpt_dic["swithing_pw"],
                                    "Leakage": pwrpt_dic["leakage_pw"],
                                    "Lotal": pwrpt_dic["total_pw"]})
    return rpt_dic

def gen_ew_dic(dic):
    """gen dc.log error and warning info dic"""
    ew_dic, count = {}, 0
    for ew_type, ew_lst in dic.items():
        ew_num = len(ew_lst)
        ew_dic[ew_type] = ew_num
        count += ew_num
    ew_dic['ew_num'] = count
    return ew_dic

def query_ew_dic(dcrun_qs):
    """generate dc.log detail infomation table"""
    model_lst = []
    if dcrun_qs.exists():
        for dcrun_obj in dcrun_qs:
            model_dic = nested_dict()
            model_dic["module"] = dcrun_obj.m_name
            model_dic["cpu_time"] = dcrun_obj.cpu_time
            model_dic["run_time"] = zone_time(dcrun_obj.run_time)
            model_dic["log_path"] = dcrun_obj.dc_log
            error_dic = dcrun_obj.error_info
            warning_dic = dcrun_obj.warning_info
            if error_dic:
                model_dic['ew_info']['error'] = gen_ew_dic(error_dic)
                model_dic['status'] = 'fail'
            else:
                model_dic['ew_info']['error'] = None
                model_dic['status'] = ('running'
                                       if model_dic['cpu_time'] == 'NA' else 'pass')
            if warning_dic:
                model_dic['ew_info']['warn'] = gen_ew_dic(warning_dic)
            model_lst.append(model_dic)
    else:
        model_lst = [{'module': None,
                      'cpu_time': None,
                      'status': None,
                      'log_path': None,
                      'run_time': None,
                      'ew_info':{'warn':None,
                                 'error': None}}]
    return model_lst

class DcUserList(ListView):
    """Dc index page"""
    template_name = 'pj_app/dc.html'
    def __init__(self):
        self.user_list = []
    def get_queryset(self):
        for user_obj in User.objects.all():
            if user_obj.asic_info.get("dc"):
                self.user_list.append(user_obj.name)
    def get_context_data(self, **kwargs):
        context = super(DcUserList, self).get_context_data(**kwargs)
        context['user_list'] = self.user_list
        context['pj_type'] = 'Dc'
        context['user'] = settings.DC_USER
        context['team'] = settings.DC_TEAM
        return context

def dc_get_loginfo(request):
    """ajax---load dc log informations"""
    model = request.GET.get('model')
    user = request.GET.get('user')
    proj = request.GET.get('proj')
    module = request.GET.get('module')
    tstart = request.GET.get('tstart')
    tend = request.GET.get('tend')
    dcrun_qs = DcRun.objects.filter(user__name=user,
                                    p_name=proj,
                                    run_time__range=date_range(tstart, tend))
    if model == 'sg_md':
        dcrun_qs = dcrun_qs.filter(module__name=f"{module}___{proj}")
    model_lst = query_ew_dic(dcrun_qs)
    return HttpResponse(json.dumps(model_lst), content_type='application/json')

def dc_get_tminfo(request):
    """ajax----load different level to show startpoint to endpoint"""
    user = request.GET.get('user')
    proj = request.GET.get('proj')
    module = request.GET.get('module')
    time = request.GET.get('time')
    level = request.GET.get('level')
    dcrun_qs = DcRun.objects.filter(user__name=user,
                                    p_name=proj,
                                    module__name=f"{module}___{proj}")
    rpt_type_dic = query_tm_lvl(dcrun_qs, time, lvl=level)
    return HttpResponse(json.dumps(rpt_type_dic), content_type='application/json')

def dc_detail_loginfo(request, path):
    """load local file to show in the brower"""
    if os.path.exists(path):
        with open(path) as file:
            log_str = file.read()
    else:
        log_str = "Error: No file found"
    return render(request, 'pj_app/dc_detail_log.html',
                  {'log_str': log_str})

def dc_get_rpt(request, **kwargs):
    """singe dc report detail inormation"""
    dcrun_qs = DcRun.objects.filter(user__name=kwargs["user"],
                                    p_name=kwargs["proj"],
                                    module__name=f"{kwargs['module']}___{kwargs['proj']}")
    if kwargs["rpt_type"] == 'qor_rpt':
        rpt_type_dic = gen_qor_dic(dcrun_qs, kwargs["ref_tm"], kwargs["tar_tm"])
        return render(request, 'pj_app/dc_qor_rpt.html', {'ref_tm': kwargs["ref_tm"],
                                                          'tar_tm': kwargs["tar_tm"],
                                                          'rpt_data': rpt_type_dic})
    elif kwargs["rpt_type"] == 'tm_rpt':
        rpt_type_dic = query_tm_lvl(dcrun_qs, kwargs["ref_tm"])
        user_info = {"user": kwargs["user"],
                     "proj": kwargs["proj"],
                     "module": kwargs["module"],
                     "ref_tm": kwargs["ref_tm"]}
        return render(request, 'pj_app/dc_tm_rpt.html', {'ref_tm': kwargs["ref_tm"],
                                                         'user_info': json.dumps(user_info),
                                                         'rpt_data': rpt_type_dic})

##post data to database
@csrf_exempt
def dc_query_insert_case(request):
    """post data to database interface"""
    if request.method == 'POST':
        dc_dic = json.loads(request.body.decode())
        user_obj, _ = User.objects.update_or_create(name=dc_dic['user'])
        update_userinfo('dc', user_obj, dc_dic['proj'], dc_dic['design_name'])
        proj_obj, _ = Proj.objects.update_or_create(name=dc_dic['proj'])
        module_obj, _ = Module.objects.update_or_create(
            name=f"{dc_dic['design_name']}___{dc_dic['proj']}")
        rtime = pytz.timezone(settings.TIME_ZONE).localize(
            dt.datetime.fromtimestamp(dc_dic['run_time']))
        dcrun_qs = DcRun.objects.filter(run_time=rtime)
        if dcrun_qs.exists():
            dcrun_obj = dcrun_qs.first()
            dcrun_obj.cpu_time = dc_dic['cpu_usage']
        else:
            dcrun_obj = DcRun.objects.create(
                user=user_obj,
                proj=proj_obj,
                module=module_obj,
                p_name=dc_dic['proj'],
                m_name=dc_dic['design_name'],
                clock=dc_dic['clk_freq'],
                cpu_time=dc_dic['cpu_usage'],
                dc_log=dc_dic['dc_log'].get('log_path', ""),
                run_time=rtime)
        dcrun_obj.error_info = dc_dic['dc_log'].get('error', {})
        dcrun_obj.warning_info = dc_dic['dc_log'].get('warning', {})
        if dc_dic['status'] == 'finished':
            dcrun_obj.time_rpt = dc_dic.get('tm_rpt', {})
            dcrun_obj.qor_rpt = dc_dic.get('qor_rpt', {})
            dcrun_obj.power_rpt = dc_dic.get('pw_rpt', {})
        dcrun_obj.save()
    return HttpResponse(json.dumps({}), content_type='application/json')
