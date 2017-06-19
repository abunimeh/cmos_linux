from django.contrib import admin

# Register your models here.
from .models import Proj, Auth, Level, Group, User, Dir, Repos
class ReposAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class ProjAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class AuthAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class LevelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'repos', 'proj', 'level', 'group', 'date']
    list_filter = ['name']
    search_fields = ['name']

class DirAdmin(admin.ModelAdmin):
    list_display = ['name', 'repos', 'proj', 'level', 'group', 'auth', 'date']
    list_filter = ['name']
    search_fields = ['name']

admin.site.register(Proj, ProjAdmin)
admin.site.register(Repos, ReposAdmin)
admin.site.register(Auth, AuthAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Dir, DirAdmin)
