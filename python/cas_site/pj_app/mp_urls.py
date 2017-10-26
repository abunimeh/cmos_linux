""" mp urls"""
from django.conf.urls import url
from . import mp_views

urlpatterns = [
    url(r'^mp/$', mp_views.MpUserList.as_view(), name='mp_user'),
    url(r'^mp/ajax_loginfo/$', mp_views.mp_get_loginfo, name='mp_get_loginfo'),
    url(r'^mp/lines_rt/$', mp_views.mp_rt_ajax_lns, name='mp_rt_ajax_lns'),
    url(r'^mp/lines_formdata/$', mp_views.mp_form_ajax_lns, name='mp_form_ajax_lns'),
    url(r'^mp/data_lines/(?P<pk_str>.+)$', mp_views.mp_sg_data, name='mp_sg_data'),
    url(r'^mp/data_columns/(?P<pk_str>.+)/$', mp_views.mp_rows_data, name='mp_rows_data'),
    url(r'^mp/db_query/query_insert_case/$', mp_views.mp_query_insert_case,
        name='mp_query_insert_case'),
]
