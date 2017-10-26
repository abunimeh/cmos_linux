from django.conf.urls import url
from . import svn_views


urlpatterns = [
    ##########svn##########     
    url(r'^svn/user_info/$', svn_views.svn_user_info, name='svn_userinfo'),
    url(r'^svn/query_select/$', svn_views.svn_query_select, name = 'svn_query_select' ),
    url(r'^svn/ajax_query/$', svn_views.svn_ajax_userinfo, name = 'svn_ajax_userinfo' ),
    url(r'^svn/user_query/$', svn_views.svn_user_query, name = 'svn_user_query'),
    url(r'^svn/user_add/$', svn_views.svn_user_add, name = 'svn_user_add' ),
    url(r'^svn/(?P<pk>\w+)/change/$', svn_views.svn_user_update, name = 'svn_user_update' ),
    url(r'^svn/(?P<pk>\w+)/delete/$', svn_views.svn_user_delete, name = 'svn_user_delete' ),
    url(r'^svn/items_add_or_change/(?P<pk>\w+)/(?P<items>\w+)/$', svn_views.svn_items_add_update, name = 'svn_items_add_update' ),
    url(r'^db/query_insert_dir/$', svn_views.query_insert_dir, name='query_insert_dir'),
    url(r'^db/query_insert_user/$', svn_views.query_insert_user, name='query_insert_user'), 
    url(r'^svn/query_dir_lst/$', svn_views.svn_query_dir_lst, name='query_dir_lst'), 
]
