from django.shortcuts import get_object_or_404
from .models import User, Proj, Module, Group, Case, Sim
from django.views.generic import ListView, DetailView
from django.conf import settings
import pytz
import datetime as dt

# Create your views here.

def gen_date_range(date_str):
    tz = pytz.timezone(settings.TIME_ZONE)
    if len(date_str) == 10:
        bt = dt.datetime.strptime(date_str, '%Y_%m_%d')
        et = bt+dt.timedelta(days=1)
    else:
        bt = dt.datetime.strptime(date_str, '%Y_%m_%d_%H_%M_%S')
        et = bt+dt.timedelta(seconds=1)
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

def gen_model_dic(model, sim_obj_qs, sim_fk):
    sim_obj_qs = sim_obj_qs.order_by('case_id', 'seed', '-pub_date').distinct('case_id', 'seed')
    model_dic = {}
    for sim_obj in sim_obj_qs:
        model_obj = getattr(sim_obj, sim_fk.lower())
        if model_obj not in model_dic:
            model_dic[model_obj] = {'pn': 0, 'tn': 0, 'pr': 0, 'bc': gen_pr_color(0)}
        if sim_obj.simu_status == 'passed':
            model_dic[model_obj]['pn'] += 1
        model_dic[model_obj]['tn'] += 1
    for model_obj, model_pr_dic in model_dic.items():
        dv = model_pr_dic['pn']/model_pr_dic['tn'] if model_pr_dic['tn'] else 0
        model_pr_dic['pr'] = round(100*dv, 2)
        model_pr_dic['bc'] = gen_pr_color(model_pr_dic['pr'])
    return model_dic

def gen_sim_dic(sim_obj_qs):
    sim_obj_qs = sim_obj_qs.order_by('case_id', 'seed', '-pub_date').distinct('case_id', 'seed')
    sim_dic = {}
    for sim_obj in sim_obj_qs:
        sim_dic[sim_obj] = {
            'cn': sim_obj.case.cname,
            'gn': sim_obj.group.gname}
        if sim_obj.simu_status == 'passed':
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

class UserList(ListView):
    model = User

class DateList(ListView):
    template_name = 'regr/date_list.html'
    def get_queryset(self):
        self.user = self.kwargs['user']
        sim_obj_qs = Sim.objects.filter(user__name=self.user)
        self.day_date_qs = sim_obj_qs.dates('pub_date', 'day')
        self.time_date_qs = sim_obj_qs.datetimes('pub_date', 'second')
    def get_context_data(self, **kwargs):
        context = super(DateList, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['day_date_qs'] = self.day_date_qs
        context['time_date_qs'] = self.time_date_qs
        return context

class ProjList(ListView):
    template_name = 'regr/proj_list.html'
    def get_queryset(self):
        self.user = self.kwargs['user']
        self.date = self.kwargs['date']
        self.sim_obj_qs = Sim.objects.filter(user__name=self.user).filter(
            pub_date__range=gen_date_range(self.date))
    def get_context_data(self, **kwargs):
        context = super(ProjList, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['date'] = self.date
        context['proj_dic'] = gen_model_dic(Proj, self.sim_obj_qs, 'proj')
        return context

class ModuleList(ListView):
    template_name = 'regr/module_list.html'
    def get_queryset(self):
        self.user = self.kwargs['user']
        self.date = self.kwargs['date']
        self.proj = self.kwargs['proj']
        self.sim_obj_qs = Sim.objects.filter(user__name=self.user).filter(
            pub_date__range=gen_date_range(self.date)).filter(proj__name=self.proj)
    def get_context_data(self, **kwargs):
        context = super(ModuleList, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['date'] = self.date
        context['proj'] = self.proj
        context['module_dic'] = gen_model_dic(Module, self.sim_obj_qs, 'module')
        return context

class CaseList(ListView):
    template_name = 'regr/case_list.html'
    def get_queryset(self):
        self.user = self.kwargs['user']
        self.date = self.kwargs['date']
        self.proj = self.kwargs['proj']
        self.module = self.kwargs['module']
        self.sim_obj_qs = Sim.objects.filter(user__name=self.user).filter(
            pub_date__range=gen_date_range(self.date)).filter(proj__name=self.proj).filter(
                module__name=self.module+'___'+self.proj)
    def get_context_data(self, **kwargs):
        context = super(CaseList, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['date'] = self.date
        context['proj'] = self.proj
        context['module'] = self.module
        context['sim_dic'] = gen_sim_dic(self.sim_obj_qs)
        return context

import os
class LogList(ListView):
    template_name = 'regr/log_list.html'
    def get_queryset(self):
        self.user = self.kwargs['user']
        self.date = self.kwargs['date']
        self.proj = self.kwargs['proj']
        self.module = self.kwargs['module']
        self.log_path = self.kwargs['log_path']
    def get_context_data(self, **kwargs):
        context = super(LogList, self).get_context_data(**kwargs)
        context['user'] = self.user
        context['date'] = self.date
        context['proj'] = self.proj
        context['module'] = self.module
        context['log_path'] = self.log_path
        if os.path.isfile(self.log_path):
            if self.log_path.endswith('.log'):
                with open(self.log_path) as f:
                    context['log'] = f.read()
            else:
                context['log'] = 'only log files can be checked :)'
        else:
            context['log'] = 'log file {0} is NA'.format(self.log_path)
        return context
