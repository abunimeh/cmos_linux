""" pj app url"""
from django.conf.urls import url
from . import views
from . import regr_urls, dc_urls, fm_urls, mp_urls

urlpatterns = [
    url(r'^pj/ajax_info/$', views.pj_ajax_info, name='pj_ajax_info'),
    url(r'^pj/select/(?P<pj_type>\w+)$', views.query_select, name='query_select'),
    url(r'^$', views.PjList.as_view(), name='user'),
] + regr_urls.urlpatterns + dc_urls.urlpatterns + fm_urls.urlpatterns + mp_urls.urlpatterns
