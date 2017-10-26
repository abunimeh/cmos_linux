"""cas_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login_auth, name='login_auth'),
    url(r'^logout/', views.logout_auth, name='logout_auth'),
    url(r'^pj_app/', include('pj_app.urls', namespace='pj_app')),
    url(r'^user_info/', include('user_info.urls', namespace='user_info')),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^comments/', views.comments, name='comments'),
    url(r'^page_error/$', views.page_error, name='page_error'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'cas_site.views.page_not_found'
