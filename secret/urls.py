#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'secret.views.home'),
    url(r'^login/', 'secret.views.login'),
    url(r'^register/', 'secret.views.register'),
    url(r'^logout/', 'secret.views.logout'),
    url(r'^profile/', 'secret.views.profile'),
    url(r'^shell/ban/', 'secret.views.shell.secret_ban'),
    url(r'^shell/starlight/', 'secret.views.shell.starlight'),
    url(r'^preview/', 'secret.views.preview'),
    url(r'^faq/', 'secret.views.faq'),
    url(r'^me/', 'secret.views.me'),
    url(r'^aboutme/', 'secret.views.aboutme'),
    url(r'^cool_down/', 'secret.views.shell.cool_down'),
    url(r'^get_preview_num/', 'secret.views.shell.get_preview_num'),
    url(r'^chatboard/', 'secret.views.chatboard'),
)
