# -*- coding: utf-8 -*-
from django.core import serializers
from django.core.serializers import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from appApi.models import Config
from commonService.views import AjaxResponseMixin
from django.views.generic import TemplateView, View, FormView
from commonService.views import ajax_login_required
import random

from forms import UserLoginForm, UserRegisterForm

SESSION_KEY = '_auth_user_id'
HASH_SESSION_KEY = '_auth_user_hash'


class UserLoginView(FormView, AjaxResponseMixin):

    http_method_names = ['post']
    form_class = UserLoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        self.request.session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        context = {
            'msg': u'登录成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})


class UserLoginOutView(View, AjaxResponseMixin):

    http_method_names = ['post',]

    @method_decorator(ajax_login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        self.request.session[HASH_SESSION_KEY] = None
        return self.ajax_response({'msg': u'登出成功'})


class UserRegisterView(FormView, AjaxResponseMixin):
    http_method_names = ['post']
    form_class =UserRegisterForm


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        context = {
            'status':'success',
            'msg': u'注册成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})

class MobileCodeView(DetailView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        code_result =self.get_code()
        request.session["code"]= code_result
        data = {
            'code' : code_result
        }
        return self.ajax_response(data)

    def get_code(self):
        code_result =""
        for i in range(6):
            code_result.append(random.uniform(0, 9))
        return code_result


class AppConfigView(View, AjaxResponseMixin):

     def  get(self, request, *args, **kwargs):
           print 'hhh'
           config = Config.objects.all()[0]
           data_result = {
               'android_version':config.android_version,
               'android_url' : config.android_url,
               'android_notes' : config.android_notes,
               'android_radio' : config.android_radio
           }
           data = {
               'data' : data_result
           }
           return self.ajax_response(data)




