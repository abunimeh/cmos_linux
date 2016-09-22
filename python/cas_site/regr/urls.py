from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.UserList.as_view(), name='user'),
    url(r'^(?P<user>\w+)/$', views.DateList.as_view(), name='date'),
    url(r'^(?P<user>\w+)/(?P<date>\w+)/$', views.ProjList.as_view(), name='proj'),
    url(r'^(?P<user>\w+)/(?P<date>\w+)/(?P<proj>\w+)/$', views.ModuleList.as_view(), name='module'),
    url(r'^(?P<user>\w+)/(?P<date>\w+)/(?P<proj>\w+)/(?P<module>\w+)$', views.CaseList.as_view(), name='case'),
    url(r'^(?P<user>\w+)/(?P<date>\w+)/(?P<proj>\w+)/(?P<module>\w+)/log__(?P<log_path>[./\w]+)$', views.LogList.as_view(), name='log'),
]
