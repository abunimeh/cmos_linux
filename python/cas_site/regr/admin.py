from django.contrib import admin

# Register your models here.

from .models import User, Proj, Module, Group, Case, Sim

class UserAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class ProjAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'dleader', 'vleader']
    list_filter = ['name']
    search_fields = ['name']

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'downer', 'vowner']
    list_filter = ['name']
    search_fields = ['name']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class CaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    list_filter = ['name']
    search_fields = ['name']

class SimAdmin(admin.ModelAdmin):
    list_display = ['pub_date', 'case', 'proj_cl', 'seed', 'dut_ana_status', 'tb_ana_status', 'elab_status', 'simu_status']
    list_filter = ['pub_date']
    search_fields = ['proj_cl', 'seed', 'dut_ana_status', 'tb_ana_status', 'elab_status', 'simu_status']

admin.site.register(User, UserAdmin)
admin.site.register(Proj, ProjAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Sim, SimAdmin)
