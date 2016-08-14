# -*- coding: utf-8 -*-

from django.conf.urls import url


from views import UserLoginView
from views import AppConfigView
from views import UserResetPswdView
from views import UserLoginOutView
from views import UserLoginView
from views import UserRegisterView
from views import MobileCodeView
from views import AddCategoryItem
from views import UpdateGoodsView

urlpatterns  = (
    url(r'^user/login/$',UserLoginView.as_view()),
    url(r'^user/login_out/$',UserLoginOutView.as_view()),
    url(r'^user/registaction/$', UserRegisterView.as_view()),
    url(r'^user/mobilecode/$', MobileCodeView.as_view()),
    url(r'^index/updateconfig/$', AppConfigView.as_view()),
    url(r'^user/resetpswdbyphone/$', UserResetPswdView.as_view()),
    url(r'^category/add/$', AddCategoryItem.as_view()),
    url(r'^good/add/$', AddCategoryItem.as_view()),
    url(r'^good/update/$', UpdateGoodsView.as_view()),
    )