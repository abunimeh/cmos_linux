""" dc urls"""
from django.conf.urls import url
from . import dc_views

urlpatterns = [
    url(r'^dc/$', dc_views.DcUserList.as_view(), name='dc_user'),
    url(r'^dc/ajax_loginfo/$', dc_views.dc_get_loginfo, name='dc_get_loginfo'),
    url(r'^dc/ajax_tminfo/$', dc_views.dc_get_tminfo, name='dc_get_tminfo'),
    url(r'^dc/(?P<user>\w+)/(?P<proj>\w+)/(?P<module>\w+)/(?P<ref_tm>\w+)/(?P<tar_tm>\w+)/'
        r'(?P<rpt_type>\w+)/$', dc_views.dc_get_rpt, name='dc_get_rpt'),
    url(r'^dc/local_log_(?P<path>[\./\w]+)$', dc_views.dc_detail_loginfo,
        name='dc_detail_loginfo'),
    url(r'^dc/db_query/query_insert_case/$', dc_views.dc_query_insert_case,
        name='dc_query_insert_case'),
]
