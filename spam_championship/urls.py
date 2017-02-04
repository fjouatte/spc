"""spam_championship URL Configuration

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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from spc import views as spc_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', spc_views.home),
    url(r'^editions/', spc_views.editions),
    url(r'^edition/(?P<pk>\d+)$', spc_views.LireEdition.as_view()),
    url(r'^rules/', spc_views.rules),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^login/$', spc_views.user_login, name='login'),
    url(r'^subscribe/$', spc_views.subscribe, name='subscribe'),
    url(r'^unsubscribe/$', spc_views.unsubscribe, name='unsubscribe'),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^register/$', spc_views.register, name='register'),
    url(r'^edit/$', spc_views.edit, name='edit'),

    # login / logout urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
    url(r'^logged_out/', spc_views.logged_out, name='logged_out'),


    # change password urls
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),

    # restore password urls
    url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
