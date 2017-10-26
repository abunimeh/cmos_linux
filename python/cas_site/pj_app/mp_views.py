"""mp views"""
import datetime as dt
import collections
import json
import math
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .views import date_range, zone_time, update_userinfo
from .models import User, Proj, Module, MpRun

def gen_mp_dic(mp_qs):
    """gen mp queryset dict"""
    model_lst = []
    if mp_qs.exists():
        for mp_dic in mp_qs.values("pk", "run_time",
                                   "misc", "props",
                                   "pj_props"):
            model_lst.append(
                {"pk": mp_dic["pk"],
                 "run_time": zone_time(mp_dic["run_time"]),
                 "misc": mp_dic["misc"],
                 "props": mp_dic["props"],
                 "pj_props": mp_dic["pj_props"]})
    else:
        model_lst = [
            {"pk": None,
             "run_time": None,
             "misc": None,
             "props": None,
             "pj_props": None}]
    return model_lst

def extract_same_key(lst):
    """extraxt same keys of dicts"""
    items_dic = collections.defaultdict(list)
    key_set = lst[0].keys()
    for dic in lst[1:]:
        key_set = key_set & dic.keys()
    if key_set:
        for skey in key_set:
            val_lst = []
            for dic in lst:
                val_lst.append(dic.get(skey))
            items_dic["y_axis"].append({"name": skey, "data": val_lst})
        for dic in lst:
            dic = {key: dic[key] for key in dic.keys() - key_set}
            items_dic["ny_axis"].append(dic)
    return items_dic

def col_tab_distinct(plot_dic, items_dic):
    """merge cases info to generate table and column"""
    if not plot_dic.get("nodata"):
        for axis, val in items_dic.items():
            if axis == "cases_items":
                sm_keys = extract_same_key(val)
                if sm_keys:
                    plot_dic["y_tag"] = True
                    plot_dic["y_cnm"] = sm_keys
                else:
                    plot_dic["y_tag"] = False
                    plot_dic["y_cnm"] = val
            elif axis == "x_axis":
                plot_dic["x_max"] = max(val)
            elif axis == "interval":
                plot_dic["intv_max"] = max(val)
    return plot_dic

def get_elem_loc(key_lst, clk):
    """get element location in the list"""
    slice_loc = len(key_lst)
    if key_lst[-1] > clk:
        slice_loc = round(clk/key_lst[-1] * len(key_lst))
    if slice_loc == 0:
        slice_loc = 1
    return slice_loc

def gen_clk_intv_data(mp_dic, st_pt=None):
    """get parameters percentage in fixed interval clk"""
    loc_st = 0
    mp_data_dic = collections.defaultdict(list)
    x_lst = mp_dic["x_axis"]
    x_lst = x_lst[:x_lst.index(max(x_lst))+1]
    if st_pt:
        loc_st = get_elem_loc(x_lst, st_pt)
    else:
        loc_st = len(x_lst)
    for mp_k, mp_v in mp_dic.items():
        if mp_k == "x_axis":
            mp_data_dic[mp_k] = mp_v
        elif mp_k not in ("pkg_nums", "lst_nums"):
            for mp_kk, mp_vv in mp_v.items():
                mp_data_dic[mp_kk] = mp_vv[loc_st-1]
        else:
            mp_data_dic[mp_k] = mp_v
    return mp_data_dic

def insertion_search(lst, st_pt):
    """search point package"""
    low = 0
    high = len(lst) -1
    while low < high:
        for mp_k, mp_v in lst[low]["x_axis"].items():
            if mp_k.startswith("time"):
                low_val = mp_v[0]
        for mp_k, mp_v in lst[high]["x_axis"].items():
            if mp_k.startswith("time"):
                high_val = mp_v[-1] if mp_v[-1] else max(mp_v)
        mid = low + int((high -low)*(st_pt-low_val)/(high_val-low_val))
        for mp_k, mp_v in lst[mid]["x_axis"].items():
            if mp_k.startswith("time"):
                if st_pt > (mp_v[-1] if mp_v[-1] else max(mp_v)):
                    low = mid + 1
                elif st_pt < mp_v[0]:
                    high = mid - 1
                else:
                    return mid
    return low

def search_point_data(mp_lst, st_pt):
    """search point package data"""
    if mp_lst[-1].get("x_axis", None):
        for mp_k, mp_v in mp_lst[-1]["x_axis"].items():
            if not mp_k.startswith("time"):
                continue
            if max(mp_v) < st_pt:
                mp_lst = [mp_lst[-1]]
            else:
                index = insertion_search(mp_lst, st_pt)
                mp_lst = [mp_lst[index]]
    else:
        mp_lst = []
    return mp_lst

def gen_sg_col_data(mp_obj, st_pt=None):
    """query each rows extra data to generate column"""
    mp_dic = collections.defaultdict(list)
    mp_lst = mp_obj.data
    if mp_lst:
        y_dic = collections.defaultdict(list)
        mp_dic["pkg_nums"] = len(mp_lst)
        if st_pt:
            mp_lst = search_point_data(mp_lst, st_pt)
        else:
            mp_lst = mp_lst[-2:]
        for data in mp_lst:
            for mp_k, mp_v in data.items():
                for mp_kk, mp_vv in mp_v.items():
                    if mp_k == "x_axis" and mp_kk.startswith("time"):
                        mp_dic["lst_nums"] = len(mp_vv)
                        mp_dic[mp_k].extend(mp_vv)
                    elif mp_k == "y_axis":
                        y_dic[mp_kk].extend(mp_vv)
                if mp_k == "y_axis":
                    mp_dic[mp_k] = y_dic
        if mp_dic.get("x_axis", None) and mp_dic.get("y_axis", None):
            mp_dic = gen_clk_intv_data(mp_dic, st_pt)
        else:
            mp_dic = {}
    return mp_dic

def queryset_slice(lst, st_pt, ed_pt, cnt):
    """slice queryset based on (st_pt, ed_pt)"""
    if st_pt:
        if ed_pt:
            lst = lst[int(st_pt)-1:int(ed_pt)]
        else:
            lst = lst[int(st_pt)-1:]
    else:
        if ed_pt:
            lst = lst[:int(ed_pt)]
        else:
            lst = lst[cnt-1:]
    return lst

def gen_sg_ln_data(mp_obj, st_pt=None, ed_pt=None):
    """query each rows extra data to  generate lines"""
    mp_data_dic = collections.defaultdict(list)
    mp_data_lst = mp_obj.data
    if mp_data_lst:
        mp_dic = {}
        x_dic = collections.defaultdict(list)
        y_dic = collections.defaultdict(list)
        mp_data_dic["strk_cn"] = len(mp_data_lst)
        mp_data_dic["clk_intv"] = mp_obj.props.get("sample_interval",
                                                   "NA")
        mpjson_lst = queryset_slice(mp_data_lst,
                                    st_pt, ed_pt,
                                    mp_data_dic["strk_cn"])
        for data in mpjson_lst:
            for mp_k, mp_v in data.items():
                for mp_kk, mp_vv in mp_v.items():
                    mp_data_dic["intv_nums"] = len(mp_vv)
                    if mp_k == "x_axis":
                        x_dic[mp_kk] += mp_vv
                    elif mp_k == "y_axis":
                        y_dic[mp_kk] += mp_vv
                if mp_k == "x_axis":
                    mp_dic[mp_k] = x_dic
                elif mp_k == "y_axis":
                    mp_dic[mp_k] = y_dic
        for mp_k, mp_v in mp_dic.items():
            if mp_k == "x_axis":
                mp_data_dic[mp_k] = dict(mp_v)
            elif mp_k == "y_axis":
                for mp_kk, mp_vv in mp_v.items():
                    mp_data_dic["y_axis"].append({"name":mp_kk, "data":mp_vv})
    return mp_data_dic

def gen_rtl_data(mp_data_dic):
    """gen real time data format"""
    rtl_dic = {}
    if mp_data_dic.get("x_axis", None):
        for x_axis, lst in mp_data_dic.get("x_axis").items():
            if "time" in x_axis:
                x_point = max(lst)
        for y_axis, lst in mp_data_dic.get("y_axis").items():
            rtl_dic[y_axis] = [x_point, max(lst)]
    return rtl_dic

class MpUserList(ListView):
    """mp index """
    template_name = 'pj_app/mp.html'
    def __init__(self):
        self.user_list = []
    def get_queryset(self):
        for user_obj in User.objects.all():
            if user_obj.asic_info.get("mp"):
                self.user_list.append(user_obj.name)
    def get_context_data(self, **kwargs):
        context = super(MpUserList, self).get_context_data(**kwargs)
        context['user_list'] = self.user_list
        context['pj_type'] = 'Mp'
        context['user'] = settings.MP_USER
        context['team'] = settings.MP_TEAM
        return context

def mp_get_loginfo(request):
    """ ajax load case info"""
    user = request.GET.get('user')
    proj = request.GET.get('proj')
    module = request.GET.get('module')
    tstart = request.GET.get('tstart')
    tend = request.GET.get('tend')
    mp_obj_qs = MpRun.objects.filter(user__name=user,
                                     p_name=proj,
                                     run_time__range=date_range(tstart, tend))
    if module:
        mp_obj_qs = mp_obj_qs.filter(module__name=f"{module}___{proj}")
    model_lst = gen_mp_dic(mp_obj_qs)
    return JsonResponse(model_lst, safe=False)

def mp_rows_data(request, pk_str):
    """Many cases parameters compare"""
    plot_dic = collections.defaultdict(list)
    items_dic = collections.defaultdict(list)
    if pk_str == "ajax":
        pk_lst = request.GET.getlist("pks[]")
        x_dot = request.GET.get("x_axis")
    else:
        pk_lst = pk_str.split("*")
    plot_dic["pk_lst"] = pk_lst
    for pk_num in pk_lst:
        mp_obj_qs = MpRun.objects.filter(pk=pk_num)
        if not mp_obj_qs.exists():
            continue
        mp_obj = mp_obj_qs.first()
        case_dic = {
            "cname": mp_obj.pj_props['c_name'],
            "vname": mp_obj.pj_props['v_name'],
            "rtime": zone_time(mp_obj.run_time)
        }
        case_tm = f"{case_dic['cname']}|{case_dic['vname']}|{case_dic['rtime']}"
        row_data = (gen_sg_col_data(mp_obj) if pk_str != "ajax"
                    else gen_sg_col_data(mp_obj, st_pt=int(x_dot)))
        if not row_data:
            plot_dic["nodata"] = True
            plot_dic["case_nm"] = case_tm
            break
        plot_dic["x_axis"].append(case_tm)
        plot_dic["props"].append({case_tm: mp_obj.props})
        x_val = row_data["x_axis"]
        items_dic["x_axis"].append(max(x_val))
        items_dic["interval"].append(math.ceil(row_data["pkg_nums"]*row_data["lst_nums"]
                                               *(x_val[1] - x_val[0])/100000))
        row_data = {key: row_data[key] for key in row_data.keys() -
                    {"x_axis", "pkg_nums", "lst_nums"}}
        items_dic["cases_items"].append(row_data)
    plot_dic = col_tab_distinct(plot_dic, items_dic)
    if pk_str == "ajax":
        return JsonResponse(plot_dic)
    return render(request, 'pj_app/mp_columns.html', {"plot_data": plot_dic})

def mp_sg_data(request, pk_str):
    """get one case detail data info"""
    plot_dic = collections.defaultdict(list)
    pk_lst = pk_str.split("*")
    for pk_num in pk_lst:
        mp_obj_qs = MpRun.objects.filter(pk=pk_num)
        if not mp_obj_qs.exists():
            continue
        mp_obj = mp_obj_qs.first()
        case_tm = f"{mp_obj.pj_props['c_name']}__{zone_time(mp_obj.run_time)}"
        row_data = gen_sg_ln_data(mp_obj)
        if row_data.get("x_axis", None) and row_data.get("y_axis", None):
            row_data["pk_lst"].append(pk_num)
            plot_dic[case_tm] = row_data
    return render(request, 'pj_app/mp_lines.html', {"plot_data": dict(plot_dic)})

def mp_form_ajax_lns(request):
    """form ajax load one case to show parameters lines"""
    plot_dic = {}
    st_pt = request.GET.get("st_pt")
    ed_pt = request.GET.get("ed_pt")
    pk_str = request.GET.get("id_nums")
    mp_obj_qs = MpRun.objects.filter(pk=pk_str)
    if mp_obj_qs.exists():
        mp_obj = mp_obj_qs.first()
        row_data = gen_sg_ln_data(mp_obj, st_pt=st_pt, ed_pt=ed_pt)
        if row_data.get("x_axis", None) and row_data.get("y_axis", None):
            plot_dic = row_data
    return JsonResponse(plot_dic)

def mp_rt_ajax_lns(request):
    """real time monitor data"""
    rtl_dic = {}
    pk_str = request.GET.get("id_nums")
    gp_cn = request.GET.get("gp_cn", None)
    mp_obj_qs = MpRun.objects.filter(pk=pk_str)
    if mp_obj_qs.exists():
        mp_data_lst = mp_obj_qs.first().data
        mpjson_cnt = len(mp_data_lst)
        if gp_cn:
            gp_cn = int(gp_cn)
            if gp_cn <= mpjson_cnt:
                mp_data_dic = mp_data_lst[gp_cn-1]
                rtl_dic = gen_rtl_data(mp_data_dic)
        else:
            rtl_dic = {"pkg_st": mpjson_cnt}
    return JsonResponse(rtl_dic, safe=False)

@csrf_exempt
def mp_query_insert_case(request):
    """post data to database"""
    if request.method == 'POST':
        mp_dic = json.loads(request.body.decode())
        if mp_dic.get("case") and mp_dic.get("data"):
            proj_nm = mp_dic['case']['pj_props']['proj_name']
            m_mn = mp_dic['case']['pj_props']['m_name']
            user_obj, _ = User.objects.update_or_create(
                name=mp_dic['case']['pj_props']['user_name'])
            update_userinfo('mp', user_obj, proj_nm, m_mn)
            proj_obj, _ = Proj.objects.update_or_create(
                name=proj_nm)
            module_obj, _ = Module.objects.update_or_create(
                name=f"{m_mn}___{proj_nm}")
            rtime = pytz.timezone(settings.TIME_ZONE).localize(
                dt.datetime.fromtimestamp(mp_dic['case']['pj_props']['pub_date']))
            mp_obj, _ = MpRun.objects.update_or_create(
                user=user_obj,
                proj=proj_obj,
                module=module_obj,
                p_name=proj_nm,
                m_name=m_mn,
                run_time=rtime,
                pj_props=mp_dic['case']['pj_props'],
                props=mp_dic['case']['props'])
            mp_obj.misc = mp_dic['case']['misc']
            if mp_obj.data:
                mp_obj.data.append(mp_dic['data'])
            else:
                mp_obj.data = [mp_dic['data']]
            mp_obj.save()
    return JsonResponse({})
