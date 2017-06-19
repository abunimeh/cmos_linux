"""regr urls"""
from django.conf.urls import url
from . import regr_views

urlpatterns = [
    url(r'^regr/$', regr_views.RegrUserList.as_view(), name='regr_user'),
    url(r'^regr/ajax_model/$', regr_views.regr_get_model, name='regr_get_model'),
    url(r'^regr/db_query/query_case_dic/$', regr_views.regr_query_case_dic, name='query_case_dic'),
    url(r'^regr/db_query/query_insert_case/$', regr_views.regr_query_insert_case,
        name='regr_query_insert_case'),
]
