""" fm urls"""
from django.conf.urls import url
from . import fm_views

urlpatterns = [
    url(r'^fm/$', fm_views.FmUserList.as_view(), name='fm_user'),
    url(r'^fm/ajax_loginfo/$', fm_views.fm_get_loginfo, name='fm_get_loginfo'),
    url(r'^fm/db_query/query_insert_case/$', fm_views.fm_query_insert_case,
        name='fm_query_insert_case')
]
