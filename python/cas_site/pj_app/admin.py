"""pj app admins """
from django.contrib import admin

# Register your models here.
from .models import User, Proj, Module, RegrSimv, RegrCase, RegrSim, DcRun, DcError,\
DcWarning, DcTimeRpt, DcQorGroup, DcQorRpt, DcChkDsgGroup, DcChkDsgRpt, DcClkGateRpt,\
DcPowerRpt, FmRun, MpRun, MpJson

class UserAdmin(admin.ModelAdmin):
    """User"""
    list_display = ['name']
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
    list_display = ['user', 'proj', 'module', 'clock', 'cpu_time', 'run_time']
    list_filter = ['run_time']
    search_fields = ['user', 'proj', 'module', 'log_path']

class DcErrorAdmin(admin.ModelAdmin):
    """dc error informations """
    list_display = ['name', 'des', 'run', 'log_path']
    list_filter = ['name']
    search_fields = ['name', 'des']

class DcWarningAdmin(admin.ModelAdmin):
    """dc warning informations """
    list_display = ['name', 'des', 'file_name', 'line_number', 'run', 'log_path']
    list_filter = ['name']
    search_fields = ['name', 'des', 'file_name', 'line_number']

class DcTimeRptAdmin(admin.ModelAdmin):
    """dc time report"""
    list_display = ['name', 'start_point', 'end_point', 'slack', 'run', 'log_path']
    list_filter = ['name']
    search_fields = ['name', 'start_point', 'end_point', 'slack']

class DcQorGroupAdmin(admin.ModelAdmin):
    """dc qor type"""
    list_display = ['name', 'log_path', 'run']
    list_filter = ['name']
    search_fields = ['name', 'log_path', 'run']

class DcQorRptAdmin(admin.ModelAdmin):
    """dc qor details"""
    list_display = ['name', 'num', 'group']
    list_filter = ['name']
    search_fields = ['name', 'group']

class DcChkDsgGroupAdmin(admin.ModelAdmin):
    """dc check design type"""
    list_display = ['name', 'log_path', 'run']
    list_filter = ['name']
    search_fields = ['name', 'log_path', 'run']

class DcChkDsgRptAdmin(admin.ModelAdmin):
    """dc check design report"""
    list_display = ['name', 'num', 'group']
    list_filter = ['name']
    search_fields = ['name', 'group']

class DcClkGateRptAdmin(admin.ModelAdmin):
    """dc clk gate report"""
    list_display = ['clk_gate', 'gate_reg', 'ugate_reg', 'total_reg', 'run', 'log_path']
    list_filter = ['clk_gate', 'gate_reg', 'ugate_reg', 'total_reg']
    search_fields = ['clk_gate', 'gate_reg', 'ugate_reg', 'total_reg']

class DcPowerRptAdmin(admin.ModelAdmin):
    """dc power report"""
    list_display = ['lib', 'internal', 'switching', 'leakage', 'total', 'run', 'log_path']
    list_filter = ['lib', 'internal', 'switching', 'leakage', 'total']
    search_fields = ['lib', 'internal', 'switching', 'leakage', 'total']

class FmRunAdmin(admin.ModelAdmin):
    """dc fm report"""
    list_display = ['user', 'proj', 'module', 'status', 'run_time']
    list_filter = ['user', 'proj', 'module', 'status', 'run_time']
    search_fields = ['user', 'proj', 'module', 'run_time']

class MpRunAdmin(admin.ModelAdmin):
    """dc mp report"""
    list_display = ['user', 'p_name', 'm_name', 'props', 'pj_props', 'run_time']
    list_filter = ['pj_props']
    search_fields = ['props', 'pj_props']

class MpJsonAdmin(admin.ModelAdmin):
    """dc mp data report"""
    list_display = ['status', 'run']
    list_filter = ['status', 'run']
    search_fields = ['status', 'run']

admin.site.register(User, UserAdmin)
admin.site.register(Proj, ProjAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(RegrSimv, RegrSimvAdmin)
admin.site.register(RegrCase, RegrCaseAdmin)
admin.site.register(RegrSim, RegrSimAdmin)
admin.site.register(DcRun, DcRunAdmin)
admin.site.register(DcError, DcErrorAdmin)
admin.site.register(DcWarning, DcWarningAdmin)
admin.site.register(DcTimeRpt, DcTimeRptAdmin)
admin.site.register(DcQorGroup, DcQorGroupAdmin)
admin.site.register(DcQorRpt, DcQorRptAdmin)
admin.site.register(DcChkDsgGroup, DcChkDsgGroupAdmin)
admin.site.register(DcChkDsgRpt, DcChkDsgRptAdmin)
admin.site.register(DcClkGateRpt, DcClkGateRptAdmin)
admin.site.register(DcPowerRpt, DcPowerRptAdmin)
admin.site.register(FmRun, FmRunAdmin)
admin.site.register(MpRun, MpRunAdmin)
admin.site.register(MpJson, MpJsonAdmin)
