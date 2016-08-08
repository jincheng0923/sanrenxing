# -*- coding: utf-8 -*-

from django.conf.urls import url


from views import UserLoginView

urlpatterns  = (
    url(r'^user/login/$',UserLoginView.as_view()),
    )