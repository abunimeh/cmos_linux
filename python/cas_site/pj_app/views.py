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

def sql_query(sim):
    """get users from postgresql"""
    user_dic = collections.OrderedDict()
    for user_obj in User.objects.all():
        proj_lst = []
        for proj_obj in sim.objects.filter(user__name=user_obj.name).distinct('proj'):
            module_lst = []
            for module_obj in sim.objects.filter(
                    user__name=user_obj.name, proj__name=proj_obj.proj.name).distinct('module'):
                module_lst.append({"n":module_obj.m_name})
            proj_lst.append({"n":proj_obj.p_name, "s":module_lst})
        user_dic[user_obj.name] = proj_lst
    return user_dic

def query_select(request, pj_type):
    """combine sql users and ldap3 users and teams to select plugins"""
    query_lst = []
    if pj_type == 'regr':
        sim = RegrSim
    elif pj_type == 'dc':
        sim = DcRun
    elif pj_type == 'fm':
        sim = FmRun
    elif pj_type == 'mp':
        sim = MpRun
    sql_dic = sql_query(sim)
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
            time_str = dt.datetime.strftime(getattr(pj_flow_obj, order_type), '%Y_%m_%d_%H_%M_%S')
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
