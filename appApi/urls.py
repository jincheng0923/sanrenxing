# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


from views import UserLoginView

urlpatterns = patterns('',
    url(r'^user/login/$',UserLoginView.as_view()),
    )