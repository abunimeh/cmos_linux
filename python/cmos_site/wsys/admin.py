from django.contrib import admin
from django.contrib.auth.models import Permission
from wsys.models import Article
from reversion.admin import VersionAdmin

# Register your models here.

class ArticleAdmin(VersionAdmin):
    list_display = ['pub_date', 'reporter', 'category', 'headline']
    list_filter = ['pub_date']
    search_fields = ['headline', 'reporter']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Permission)
