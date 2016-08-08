# -*- coding: utf-8 -*-

from django.conf.urls import url


from views import UserLoginView
from views import UserLoginOutView

urlpatterns  = (
    url(r'^user/login/$',UserLoginView.as_view()),
    url(r'^user/login_out/$',UserLoginOutView.as_view()),
    )