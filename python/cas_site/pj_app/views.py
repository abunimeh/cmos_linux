"""Pj app views"""
import datetime as dt
import collections
import pytz
import ldap3
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.conf import settings
from nested_dict import nested_dict
from .models import User, RegrSim, DcRun, FmRun, MpRun

def do_line_profiler(view=None, extra_view=None):
    """profiler test"""
    import line_profiler
    def wrapper(view):
        """warpper"""
        def wrapped(*args, **kwargs):
            """wrapped"""
            prof = line_profiler.LineProfiler()
            prof.add_function(view)
            if extra_view:
                _ = [prof.add_function(v) for v in extra_view]
            with prof:
                resp = view(*args, **kwargs)
            prof.print_stats()
            return resp
        return wrapped
    if view:
        return wrapper(view)
    return wrapper

def update_userinfo(pj_type, user_obj, proj, module):
    """update user aisc information"""
    if pj_type in user_obj.asic_info:
        type_lst = user_obj.asic_info[pj_type]
        for proj_md in type_lst:
            if proj == proj_md["n"]:
                if {"n": module} not in proj_md["s"]:
                    for j, mod_dic in enumerate(proj_md["s"]):
                        if mod_dic["n"] > module:
                            proj_md["s"].insert(j, {"n": module})
                            break
                break
        else:
            for i, proj_dic in enumerate(type_lst):
                if proj_dic["n"] > proj:
                    type_lst.insert(i, {"n": proj, "s": [{"n": module}]})
                    break
    else:
        user_obj.asic_info[pj_type] = [{"n": proj, "s": [{"n": module}]}]
    user_obj.save()

# Create your views here.
def gen_date_range(date_str, diff=1):
    """gen datatime range"""
    diff = int(diff)
    timezone = pytz.timezone(settings.TIME_ZONE)
    if len(date_str) == 10:
        endt = dt.datetime.strptime(
            date_str, '%Y_%m_%d')+dt.timedelta(days=1)
        begt = endt-dt.timedelta(days=diff)
    else:
        endt = dt.datetime.strptime(
            date_str, '%Y_%m_%d_%H_%M_%S')+dt.timedelta(seconds=1)
        begt = endt-dt.timedelta(seconds=diff)
    begt = timezone.localize(begt)
    endt = timezone.localize(endt)
    return (begt, endt)

def date_range(tstart, tend):
    """gen start and end datetime"""
    timezone = pytz.timezone(settings.TIME_ZONE)
    begt = dt.datetime.strptime(tstart, '%Y-%m-%d')
    endt = dt.datetime.strptime(tend, '%Y-%m-%d') + dt.timedelta(days=1)
    begt = timezone.localize(begt)
    endt = timezone.localize(endt)
    return (begt, endt)

def zone_time(dt_obj):
    """gen datetime"""
    timezone = pytz.timezone(settings.TIME_ZONE)
    endt = dt_obj.astimezone(timezone)
    return dt.datetime.strftime(endt, '%Y_%m_%d_%H_%M_%S')

def ldap3_query():
    """get users and teams from ldaps"""
    server = ldap3.Server(settings.AUTH_LDAP_SERVER_URI, get_info=ldap3.ALL)
    userdn = settings.AUTH_LDAP_BIND_DN
    passwd = settings.AUTH_LDAP_BIND_PASSWORD
    c_ins = ldap3.Connection(server, user=userdn, password=passwd, auto_bind=True)
    c_ins.bind()
    c_ins.search("ou=Group,dc=sari,dc=com", '(objectclass=posixGroup)',
                 attributes=ldap3.ALL_ATTRIBUTES)
    g_entries = c_ins.entries
    g_entries.sort()
    c_ins.search("ou=People,dc=sari,dc=com", '(objectclass=person)',
                 attributes=['userPKCS12', 'gidNumber', 'uid'])
    p_entries = c_ins.entries
    p_entries.sort()
    model_dic = collections.OrderedDict()
    team_dic = collections.OrderedDict()
    for pp_entry in p_entries:
        if (pp_entry.entry_attributes_as_dict.get('userPKCS12', False) and
                (pp_entry.entry_attributes_as_dict.get('userPKCS12')[0] == b'0')):
            if pp_entry.gidNumber.value not in model_dic:
                model_dic[pp_entry.gidNumber.value] = []
                model_dic[pp_entry.gidNumber.value].append(pp_entry.uid.value)
            else:
                model_dic[pp_entry.gidNumber.value].append(pp_entry.uid.value)
    for gp_entry in g_entries:
        if gp_entry.entry_attributes_as_dict.get('description', 'none') != 'none':
            team_dic[gp_entry.cn.value] = model_dic[gp_entry.gidNumber.value]
    return team_dic

def sql_query(pj_type):
    """get users from postgresql"""
    user_dic = collections.OrderedDict()
    for user_obj in User.objects.all():
        if pj_type in user_obj.asic_info:
            user_dic[user_obj.name] = user_obj.asic_info[pj_type]
    return user_dic

def query_select(request, pj_type):
    """combine sql users and ldap3 users and teams to select plugins"""
    query_lst = []
    sql_dic = sql_query(pj_type)
    for tm_key, tm_value in ldap3_query().items():
        user_lst = []
        for user_nm in tm_value:
            if user_nm in sql_dic:
                user_lst.append(
                    {"n":user_nm, "s":sql_dic[user_nm]})
            else:
                user_lst.append(
                    {"n":user_nm, "s":[{'n': 'None', 's':[{'n': 'None'}]}]})
        team_dic = {"n": tm_key, "s": user_lst}
        query_lst.append(team_dic)
    return JsonResponse(query_lst, safe=False)

def pj_flow_info(pj_flow_qs, order_type, index):
    """get users and run time of recent three run times"""
    pj_flow_dic = nested_dict()
    number = 0
    if pj_flow_qs.objects.exists():
        for pj_flow_obj in pj_flow_qs.objects.order_by('-'+order_type)[0:index]:
            time_str = zone_time(getattr(pj_flow_obj, order_type))
            pj_flow_dic['user'][f"user{number}"] = pj_flow_obj.user.name
            pj_flow_dic['run_time'][f"time{number}"] = time_str
            number += 1
    else:
        pj_flow_dic['user'][f"user{number}"] = None
        pj_flow_dic['run_time'][f"time{number}"] = None
    return pj_flow_dic

def pj_ajax_info(request):
    """gen pj app index tables to show dc, fm, mp and so on"""
    regr_dic = pj_flow_info(RegrSim, 'pub_date', settings.PJ_TIMES)
    dc_dic = pj_flow_info(DcRun, 'run_time', settings.PJ_TIMES)
    fm_dic = pj_flow_info(FmRun, 'run_time', settings.PJ_TIMES)
    mp_dic = pj_flow_info(MpRun, 'run_time', settings.PJ_TIMES)
    data_dic = {
        "data": [
            {
                "pj_flow": "regr",
                "users": regr_dic.get('user'),
                "run_time": regr_dic.get('run_time'),
            },
            {
                "pj_flow": "dc",
                "users": dc_dic.get('user'),
                "run_time": dc_dic.get('run_time'),
            },
            {
                "pj_flow": "fm",
                "users": fm_dic.get('user'),
                "run_time": fm_dic.get('run_time'),
            },
            {
                "pj_flow": "mp",
                "users": mp_dic.get('user'),
                "run_time": mp_dic.get('run_time'),
            },
        ]
    }
    return JsonResponse(data_dic)

class PjList(ListView):
    """Pj index page function"""
    template_name = 'pj_app/pj_app.html'
    def get_queryset(self):
        pass
    def get_context_data(self, **kwargs):
        context = super(PjList, self).get_context_data(**kwargs)
        return context
