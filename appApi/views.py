# -*- coding: utf-8 -*-
from django.core import serializers
from django.core.serializers import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from appApi.models import Config
from commonService.views import AjaxResponseMixin, send_sms
from django.views.generic import TemplateView, View, FormView
from commonService.views import ajax_login_required
import random

from forms import UserLoginForm, UserRegisterForm, UserResetPswdForm, AddCategoryForm

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
    form_class = UserRegisterForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_form(self):
        return self.form_class(self.request, **self.get_form_kwargs())

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

class MobileCodeView(View, AjaxResponseMixin):
    http_method_names = ['get']
    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone')
        type = request.GET.get('type', 1)
        if phone:
            code_result = self.get_code()
            content = u'【小区超市】您的验证码是' + code_result
            is_send = send_sms(phone, content, 'test')
            if is_send:
                request.session["code"] = code_result
                data = {
                    'code': code_result
                }
                return self.ajax_response(data)
            else:
                data = {
                    'code': code_result
                }
                return self.update_errors(u'验证码发送失败')
        else :
            return self.update_errors(u'非法请求')



    def get_code(self):
        code_result =""
        for i in range(6):
            code_result=code_result+(str)(random.randint(0, 9))
        return code_result

class UserResetPswdView(FormView,AjaxResponseMixin):
    http_method_names = ['post']
    form_class = UserResetPswdForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        context = {
            'status': 'success',
            'msg': u'密码修改成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})


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



class AddCategoryItem(FormView, AjaxResponseMixin):

    form_class = AddCategoryForm

    # @ajax_login_required
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = {
            'status': 'success',
            'msg': u'目录添加成功',
        }
        form.save()
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})



