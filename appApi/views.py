# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import View, FormView
from collections import defaultdict

from appApi.models import Config
from commonService.views import AjaxResponseMixin, send_sms
from commonService.views import ajax_login_required

from forms import UserLoginForm
from forms import UserRegisterForm
from forms import UserResetPswdForm
from forms import AddCategoryForm
from forms import AddGoodForm
from forms import UpdateGoodForm
from forms import AddGood2CartForm
from forms import UpdateCartItemNumForm

from models import Community
from models import Good
from models import User
from models import CartItem

import random


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
    #商品目录

    form_class = AddCategoryForm
    http_method_names = ['post',]

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


class AddGoodsView(FormView, AjaxResponseMixin):

    '''
        :param:
            refer to good model
        添加商品
    '''

    form_class = AddGoodForm
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        context = {
            'status': 'success',
            'msg': u'商品添加成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})


class UpdateGoodsView(FormView, AjaxResponseMixin):

    '''
        修改商品信息接口
    '''

    form_class = UpdateGoodForm
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        context = {
            'status': 'success',
            'msg': u'商品修改成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})


class GoodsListView(View, AjaxResponseMixin):

    '''
        获取商品列表接口
    '''

    http_method_names = ['get']
    page_size = 10

    def get(self, request, *args, **kwargs):
        cate = request.GET.get('cate')
        comm = request.GET.get('comm')
        p = request.GET.get('p', 1)
        goods_list = self.get_query_set(cate, comm, p)
        return self.ajax_response({
            'status': 'success',
            'data': goods_list
        })

    def get_query_set(self, cate=None, comm=None, p=1):
        query = Q()
        if cate:
            query &= Q(cate=cate)
        if comm:
            query &= Q(community=comm)
        goods_query = Good.objects.filter(query).order_by('-rank')
        goods_paginator = Paginator(goods_query, self.page_size)
        goods_list = goods_paginator.page(p)
        items = goods_list.object_list
        return items


class GoodsDetailView(View, AjaxResponseMixin):

    '''
        获取商品详情接口
        参数 商品ID
    '''

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        gid = kwargs.get('gid')
        context = {}
        if not gid:
            self.update_errors('商品ID为空')
        else:
            try:
                good = Good.objects.get(pk=gid)
            except Exception as e:
                print e
                self.update_errors('商品ID错误')
            else:
                context.update({
                    'name': good.name,
                    'price': good.sale_price,
                    'pic': good.logo,
                    'inventory': good.inventory,
                })
        return self.ajax_response(context)


class CommunityListView(View, AjaxResponseMixin):

    '''
        获取小区列表
        参数 城市， 街道
    '''

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        city = request.GET.get('city')
        area = request.GET.get('area')
        query = Q(status='A')
        if city:
            query &= Q(city=city)
        if area:
            query &= Q(area=area)
        comm_list = Community.objects.fiter(query).values('id', 'name', 'address')
        comm_list_dict = map(dict, comm_list)
        return self.ajax_response({
            'data': comm_list_dict
        })


class BindUserWithCommunity(FormView, AjaxResponseMixin):

    '''
        用户绑定小区接口
        待议
    '''
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        pass

    def form_invalid(self, form):
        pass




class AddGood2Cart(FormView, AjaxResponseMixin):

    '''
        添加商品到购物车接口
        参数 good_id user_id num
    '''

    http_method_names = ['post']
    form_class = AddGood2CartForm

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = {
            'status': 'success',
            'msg': u'加入成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})


class UpdateCartItem(FormView, AjaxResponseMixin):

    '''
        修改购物车商品数量
    '''

    http_method_names = ['post']
    form_class = UpdateCartItemNumForm

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = {
            'status': 'success',
            'msg': u'修改成功',
        }
        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response({})


class GetUserCartItemList(View, AjaxResponseMixin):

    '''
        获取用户购物车列表
        参数： 用户ID
        返回：分小区
    '''

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        context = {}
        if not user_id:
            self.update_errors('用户ID为空')
        else:
            try:
                user = User.objects.get(pk=user_id)
            except Exception as e:
                print e
                self.update_errors('用户ID错误')
            else:
                cart_items = CartItem.objects.filter(user=user, status='A')
                context.update({
                    'data': self.parse_cart_item(cart_items)
                })
        return self.ajax_response(context)

    def parse_cart_item(self, items):
        comm_goods_dict = defaultdict(list)
        for item in items:
            comm_goods_dict['item.good.community.name'].append(
                    {
                        'good_name': item.good.name,
                        'num': item.num,
                        'msg': '库存不足' if item.num > item.good.inventory else '',
                        'logo': item.good.logo,
                        'price': item.good.sale_price,
                        'total_price': round(item.num * item.good.sale_price, 2)
                    }
            )
        context = []
        for k, v in comm_goods_dict.items():
            context.append({
                'comm_name': k,
                'good_list': v
            })
        return context

class CreateOrder(FormView, AjaxResponseMixin):
    pass
