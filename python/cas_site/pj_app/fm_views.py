""" fm views"""
import datetime as dt
import json
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.http import JsonResponse
from django.conf import settings
from .models import User, Proj, Module, FmRun
from .views import date_range, zone_time

def gen_fm_dic(fm_qs):
    """table row data list"""
    model_lst = []
    if fm_qs.exists():
        for fm_qs_obj in fm_qs:
            model_lst.append({
                'module': fm_qs_obj.m_name,
                'proj': fm_qs_obj.p_name,
                'status': fm_qs_obj.status,
                'run_time': zone_time(fm_qs_obj.run_time)})
    else:
        model_lst = [{'module': None, 'proj':None,
                      'status':None, 'run_time': None}]
    return model_lst

#fm index
class FmUserList(ListView):
    """fm index"""
    template_name = 'pj_app/fm.html'
    def __init__(self):
        self.user_list = []
    def get_queryset(self):
        for user_obj in FmRun.objects.distinct('user'):
            self.user_list.append(user_obj.user.name)
    def get_context_data(self, **kwargs):
        context = super(FmUserList, self).get_context_data(**kwargs)
        context['user_list'] = self.user_list
        context['pj_type'] = 'Fm'
        context['user'] = settings.FM_USER
        context['team'] = settings.FM_TEAM
        return context

def fm_get_loginfo(request):
    """ajax---load all modules of project and single module """
    model = request.GET.get('model')
    user = request.GET.get('user')
    proj = request.GET.get('proj')
    module = request.GET.get('module')
    tstart = request.GET.get('tstart')
    tend = request.GET.get('tend')
    fm_obj_qs = FmRun.objects.filter(user__name=user,
                                     p_name=proj,
                                     run_time__range=date_range(tstart, tend))
    if model == "all_mds":
        model_lst = gen_fm_dic(fm_obj_qs)
    elif model == 'sg_md':
        model_lst = gen_fm_dic(fm_obj_qs.filter(m_name=module))
    return JsonResponse(model_lst, safe=False)

##post data to database
@csrf_exempt
def fm_query_insert_case(request):
    """post data into database interface"""
    if request.method == 'POST':
        fm_dic = json.loads(request.body.decode())
        user_obj, _ = User.objects.update_or_create(name=fm_dic['user'])
        proj_obj, _ = Proj.objects.update_or_create(name=fm_dic['proj'])
        module_obj, _ = Module.objects.update_or_create(name=fm_dic['design_name'])
        rtime = pytz.timezone(settings.TIME_ZONE).localize(
            dt.datetime.fromtimestamp(fm_dic['run_time']))
        FmRun.objects.create(
            user=user_obj,
            proj=proj_obj,
            module=module_obj,
            p_name=fm_dic['proj'],
            m_name=fm_dic['design_name'],
            status=fm_dic['status'],
            run_time=rtime)
    return JsonResponse({})
