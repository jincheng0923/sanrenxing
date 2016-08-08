# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.core.serializers import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from commonService.views import AjaxResponseMixin
from django.views.generic import TemplateView, View, FormView
import random

from forms import UserLoginForm, UserRegisterForm


class UserLoginView(FormView, AjaxResponseMixin):

    http_method_names = ['post']
    form_class = UserLoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.user = form.get_user()
        user = form.get_user()
        context = {
            'msg': u'登录成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})

class UserRegisterView(FormView,AjaxResponseMixin):
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
        data = {}
        data["status"]="success"
        data["code"]=code_result
        return  HttpResponse(json.dumps(data),content_type="application/json")

    def get_code(self):
        code_result =""
        for i in range(6):
            code_result.append(random.uniform(0, 9));
        return code_result



