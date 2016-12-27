from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^db_query/query_case_dic/$', views.query_case_dic, name='query_case_dic'),
    url(r'^db_query/query_insert_case/$', views.query_insert_case, name='query_insert_case'),
    url(r'^$', views.UserList.as_view(), name='user'),
    url(r'^db_select/$', views.query_select, name='query_select'),
    url(r'^ajax_model/$', views.get_model, name='get_model'),
]
