# -*- coding: utf-8 -*-

from django.conf.urls import url


from views import UserLoginView, UserRegisterView, MobileCodeView

urlpatterns  = (
    url(r'^user/login/$',UserLoginView.as_view()),
    url(r'^user/register/$', UserRegisterView.as_view()),
    url(r'^user/getcode/$', MobileCodeView.as_view()),
    )