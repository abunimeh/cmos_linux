"""cmos_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views as ckviews

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^wsys/', include('wsys.urls', namespace='wsys')),
    url(r'^ckeditor_uploader/upload/', ckviews.upload, name='ckeditor_upload'),
    url(r'^ckeditor_uploader/browse/', never_cache(ckviews.browse),
        name='ckeditor_browse'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile/',
        TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
