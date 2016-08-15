# -*- coding: utf-8 -*-

from django.conf.urls import url

from views import AppConfigView
from views import UserResetPswdView
from views import UserLoginOutView
from views import UserLoginView
from views import UserRegisterView
from views import MobileCodeView
from views import AddCategoryItem
from views import UpdateGoodsView
from views import GoodsListView
from views import GoodsDetailView

urlpatterns = (
    url(r'^user/login/$', UserLoginView.as_view()),
    url(r'^user/login_out/$', UserLoginOutView.as_view()),
    url(r'^user/registaction/$', UserRegisterView.as_view()),
    url(r'^user/mobilecode/$', MobileCodeView.as_view()),
    url(r'^index/updateconfig/$', AppConfigView.as_view()),
    url(r'^user/resetpswdbyphone/$', UserResetPswdView.as_view()),
    url(r'^category/add/$', AddCategoryItem.as_view()),
    url(r'^good/add/$', AddCategoryItem.as_view()),
    url(r'^good/update/$', UpdateGoodsView.as_view()),
    url(r'^good/list/$', GoodsListView.as_view()),
    url(r'^good/(?P<pid>\d+)/$', GoodsDetailView.as_view()),
)
