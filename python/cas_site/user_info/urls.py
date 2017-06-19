from django.conf.urls import url
from . import ldap_urls
from . import svn_urls

urlpatterns = ldap_urls.urlpatterns + svn_urls.urlpatterns
