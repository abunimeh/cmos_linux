from django.conf.urls import url
from . import ldap_views

urlpatterns = [
    url(r'^ldap/userinfo/$', ldap_views.ldap_userinfo, name = 'ldap_userinfo' ),
    url(r'^ldap/allmembers/$', ldap_views.ldap_allmembers, name = 'ldap_allmembers' ),
    url(r'^ldap/ajaxmembers/$', ldap_views.ldap_ajaxmembers, name = 'ldap_ajaxmembers' ), 
    url(r'^ldap/useradd/$', ldap_views.ldap_useradd, name = 'ldap_useradd'),
    url(r'^ldap/userdelete/$', ldap_views.ldap_userdelete, name = 'ldap_userdelete' ),
    url(r'^ldap/memberupdate/$', ldap_views.ldap_membupdate, name = 'ldap_membupdate'),
    url(r'^ldap/passwdmodify/$', ldap_views.ldap_pdmodify, name = 'ldap_pdmodify'),
    url(r'^ldap/queryselect/(?P<team>\w+)/(?P<user>\w+)/$', ldap_views.ldap_queryselect, name = 'ldap_queryselect' ),
]
