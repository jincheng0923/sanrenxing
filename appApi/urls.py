# -*- coding: utf-8 -*-

from django.conf.urls import url


from views import UserLoginView, AppConfigView, UserResetPswdView
from views import UserLoginOutView
from views import UserLoginView, UserRegisterView, MobileCodeView

urlpatterns  = (
    url(r'^user/login/$',UserLoginView.as_view()),
    url(r'^user/login_out/$',UserLoginOutView.as_view()),
    url(r'^user/registaction/$', UserRegisterView.as_view()),
    url(r'^user/mobilecode/$', MobileCodeView.as_view()),
    url(r'^index/updateconfig/$', AppConfigView.as_view()),
    url(r'^user/resetpswdbyphone/$', UserResetPswdView.as_view()),
    )