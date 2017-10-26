"""pj app admins """
from django.contrib import admin

# Register your models here.
from .models import User, Proj, Module, RegrSimv, RegrCase, RegrSim, DcRun, FmRun, MpRun, Comment

class UserAdmin(admin.ModelAdmin):
    """User"""
    list_display = ['name', 'asic_info']
    list_filter = ['name']
    search_fields = ['name']

class ProjAdmin(admin.ModelAdmin):
    """project"""
    list_display = ['name', 'leader', 'dleader', 'vleader']
    list_filter = ['name']
    search_fields = ['name']

class ModuleAdmin(admin.ModelAdmin):
    """modules"""
    list_display = ['name', 'downer', 'vowner']
    list_filter = ['name']
    search_fields = ['name']

class RegrSimvAdmin(admin.ModelAdmin):
    """regressions simv"""
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class RegrCaseAdmin(admin.ModelAdmin):
    """regressions cases"""
    list_display = ['name', 'owner']
    list_filter = ['name']
    search_fields = ['name']

class RegrSimAdmin(admin.ModelAdmin):
    """regressions sims"""
    list_display = ['pub_date', 'end_date', 'case', 'proj_cl', 'seed', 'dut_ana_status',
                    'tb_ana_status', 'elab_status', 'simu_status']
    list_filter = ['pub_date']
    search_fields = ['proj_cl', 'seed', 'dut_ana_status',
                     'tb_ana_status', 'elab_status', 'simu_status']

class DcRunAdmin(admin.ModelAdmin):
    """dc run """
    list_display = ['user', 'proj', 'module', 'clock', 'cpu_time',
                    'run_time', 'dc_log', 'error_info', 'warning_info',
                    'time_rpt', 'qor_rpt', 'power_rpt']
    list_filter = ['run_time']
    search_fields = ['user', 'proj', 'module']

class FmRunAdmin(admin.ModelAdmin):
    """dc fm report"""
    list_display = ['user', 'proj', 'module', 'status', 'run_time']
    list_filter = ['user', 'proj', 'module', 'status', 'run_time']
    search_fields = ['user', 'proj', 'module', 'run_time']

class MpRunAdmin(admin.ModelAdmin):
    """dc mp report"""
    list_display = ['user', 'p_name', 'm_name', 'props', 'pj_props', 'misc', 'data', 'run_time']
    list_filter = ['pj_props']
    search_fields = ['props', 'pj_props']

class CommentAdmin(admin.ModelAdmin):
    """ user comment"""
    list_display = ['user', 'comment', 'pub_time']
admin.site.register(User, UserAdmin)
admin.site.register(Proj, ProjAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(RegrSimv, RegrSimvAdmin)
admin.site.register(RegrCase, RegrCaseAdmin)
admin.site.register(RegrSim, RegrSimAdmin)
admin.site.register(DcRun, DcRunAdmin)
admin.site.register(FmRun, FmRunAdmin)
admin.site.register(MpRun, MpRunAdmin)
admin.site.register(Comment, CommentAdmin)
