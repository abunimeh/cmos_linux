from django.conf.urls import include, url
from wsys import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^read/(?P<pk>\w+)/$', views.read, name='read'),
    url(r'^modi/(?P<pk>\w+)/$', views.modi, name='modi'),
    url(r'^dele/(?P<pk>\w+)/$', views.dele, name='dele'),
    url(r'^history/(?P<pk>\w+)/$', views.history, name='history'),
    url(r'^version/(?P<vpk>\w+)/(?P<pk>\w+)/$', views.version, name='version'),
    url(r'^diff/(?P<pk>\w+)/$', views.diff, name='diff'),
]
