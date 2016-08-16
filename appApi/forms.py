# coding:utf-8
import uuid
from datetime import datetime

from django import forms
from django.contrib.auth import authenticate
from models import User
from models import Category
from models import Good
from models import CartItem
from django.db import transaction


class UserLoginForm(forms.Form):

    error_messages = {
        'account_not_exist': u'该账号不存在',
        'invalid_login': u'密码错误',
    }

    account = forms.CharField(max_length=20, required=True,
                    error_messages={
                        'required': u'请输入正确手机号',
                        'max_length': u'请输入正确手机号',
                    })
    password = forms.CharField(min_length=6, max_length=20, required=True,
                    error_messages={
                        'required': u'密码错误',
                        'min_length': u'密码错误',
                        'max_length': u'密码错误',
                    })

    def clean_account(self):
        account = self.cleaned_data['account']
        try:
            user = User.objects.get(phone=account)
        except Exception as e:
            print e
            raise forms.ValidationError(self.error_messages['account_not_exist'])

        else:
            return user

    def clean(self):
        phone = self.cleaned_data.get('account', None)
        password = self.cleaned_data.get('password', None)

        if phone and password:
            self.user = authenticate(phone=phone,
                            password=password)
            if self.user is None:
                raise forms.ValidationError(
                            self.error_messages['invalid_login'])

        return self.cleaned_data

    def get_user(self):
        return self.user


class UserRegisterForm (forms.Form):
    error_messages = {
        'invalid_register': u'用户已存在',
        'invalid_code_error': u'验证码错误',
    }

    phone = forms.CharField(max_length=20, required=True,
                            error_messages={
                                  'required': u'请输入正确手机号1',
                                  'max_length': u'请输入正确手机号2',
                            })
    mobilecode = forms.CharField(min_length=6,max_length=6,required=True,
                           error_messages={
                                 'required':u'请输入验证码',
                                 'min_length':u'验证码格式不正确',
                                 'max_length':u'验证码格式不正确'
                           })

    pswd = forms.CharField(min_length=6, required=True,
                            error_messages={
                                 'required':u'请输入密码',
                                 'min_length':u'密码格式不正确',
                            })

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(self.__class__, self).__init__(*args, **kwargs)

    def clean_mobilecode(self):
        code = self.request.session.get('code')
        mobilecode = self.cleaned_data.get('mobilecode')
        print u'----------'+mobilecode
        if code != mobilecode :
            raise forms.ValidationError(
                self.error_messages['invalid_code_error'])

    def clean(self):
        phone = self.cleaned_data.get('phone')
        pswd = self.cleaned_data.get('pswd')

        if phone and pswd:
            try:
                exit_user = User.objects.get(phone=phone)
                if exit_user is None:
                    return self.cleaned_data
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_register'])
            except Exception as err:
                print(err)

    def save(self):
        account = self.cleaned_data.get('account')
        pswd = self.cleaned_data['pswd']
        user = User(phone=account, pswd=pswd,community_id=1)
        user.save()

class UserResetPswdForm(forms.Form):
    error_messages = {
        'invalid_code_error': u'验证码错误',
        'invalid_user_not_exit': u'用户不存在',
        'invalid_error': u'账户密码不能为空',
    }

    account = forms.CharField(max_length=20, required=True,
                              error_messages={
                                  'required': u'请输入正确手机号',
                                  'max_length': u'请输入正确手机号',
                              })
    code = forms.CharField(min_length=6, max_length=6, required=True,
                           error_messages={
                               'required': u'请输入验证码',
                               'min_length': u'验证码格式不正确',
                               'max_length': u'验证码格式不正确'
                           })

    pswd = forms.CharField(min_length=6, required=True,
                           error_messages={
                               'required': u'请输入密码',
                               'min_length': u'密码格式不正确',
                           })

    def clean_mobilecode(self):
        code = self.request.session.get('code')
        mobilecode = self.changed_data.get('mobilecode')
        print u'----------' + mobilecode
        if code != mobilecode:
            raise forms.ValidationError(
                self.error_messages['invalid_code_error'])

    def clean(self):
        account = self.cleaned_data.get('account')
        pswd = self.cleaned_data.get('pswd')

        if account and pswd:
            try:
                exit_user = User.objects.get(phone=account)
                if exit_user :
                    return self.cleaned_data
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_user_not_exit'])
            except Exception as err:
                print(err)
        else:
            raise forms.ValidationError(
                self.error_messages['invalid_register'])

    def update(self):
        account = self.cleaned_data.get('account')
        pswd = self.cleaned_data['pswd']
        user = User(pswd=pswd)
        user.save()


class AddCategoryForm(forms.Form):

    name = forms.CharField(required=True, error_messages={
                               'required': u'名称不能为空',
                           })
    sname = forms.CharField(required=False)
    logo = forms.CharField(required=False)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            ca = Category.objects.get(name=name)
        except Exception as e:
            print e
            return  name
        else:
            raise forms.ValidationError(u'名称已经存在')

    def save(self):
        cat = Category.objects.create(**self.cleaned_data)


class AddGoodForm(forms.Form):
    cate_id = forms.CharField(required=True, error_messages={
        'required': '父级目录不能为空',
    })
    community_id = forms.CharField(required=True, error_messages={
        'required': '所属社区不能为空',
    })
    name = forms.CharField(required=True, max_length=16, error_messages={
        'required': '商品名称不能为空',
        'max_length': '商品名称超长'
    })
    sname = forms.CharField(required=False, max_length=64, error_messages={
        'max_length': '商品名称超长'
    })
    des = forms.CharField(required=False)
    logo = forms.CharField(required=True, max_length=64, error_messages={
        'required': '缩略图不能为空',
        'max_length': '缩略图地址超长'
    })
    price = forms.DecimalField(required=False, max_digits=9, decimal_places=2)
    sale_price = forms.DecimalField(required=True, max_digits=9, decimal_places=2, error_messages={
        'required': '销售价格不能为空',
    })
    spec = forms.CharField(required=False, max_length=128)
    inventory = forms.IntegerField(required=True, error_messages={
        'required': '库存不能为空'
    })

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            Good.objects.get(name=name)
        except Exception as e:
            print e
            return name
        else:
            raise forms.ValidationError('商品名称不能重复')

    def save(self):
        good = Good.objects.create(**self.cleaned_data)


class UpdateGoodForm(forms.Form):
    good_id = forms.CharField(required=True, error_messages={
       'required': '商品ID不能为空',
    })
    cate_id = forms.CharField(required=False, error_messages={
        'required': '父级目录不能为空',
    })
    community_id = forms.CharField(required=False, error_messages={
        'required': '所属社区不能为空',
    })
    name = forms.CharField(required=False, max_length=16, error_messages={
        'required': '商品名称不能为空',
        'max_length': '商品名称超长'
    })
    sname = forms.CharField(required=False, max_length=64, error_messages={
        'max_length': '商品名称超长'
    })
    des = forms.CharField(required=False)
    logo = forms.CharField(required=False, max_length=64, error_messages={
        'required': '缩略图不能为空',
        'max_length': '缩略图地址超长'
    })
    price = forms.DecimalField(required=False, max_digits=9, decimal_places=2)
    sale_price = forms.DecimalField(required=True, max_digits=9, decimal_places=2, error_messages={
        'required': '销售价格不能为空',
    })
    spec = forms.CharField(required=False, max_length=128)
    inventory = forms.IntegerField(required=False, error_messages={
        'required': '库存不能为空'
    })

    def clean_good_id(self):
        good_id = self.cleaned_data.get('good_id')
        try:
            good = Good.objects.get(pk=good_id)
        except Exception as e:
            print e
            raise forms.ValidationError('商品ID不存在')
        else:
            self.good = good
            return good_id

    def save(self):
        self.cleaned_data.pop('good_id')
        self.good.update(**self.cleaned_data)
        self.good.save()


class AddGood2CartForm(forms.Form):

    user_id = forms.IntegerField(required=True, error_messages={
        'required': '用户ID 不能为空',
    })
    good_id = forms.IntegerField(required=True, error_messages={
        'required': '商品ID 不能为空',
    })
    num = forms.IntegerField(required=True, error_messages={
        'required': '商品数量不能为空',
    })

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            print e
            raise forms.ValidationError('用户ID错误')
        else:
            self.user = user
            return user_id

    def clean_good_id(self):
        good_id = self.cleaned_data.get('good_id')
        try:
            good = Good.objects.get(pk=good_id, status='A')
        except Exception as e:
            print e
            raise forms.ValidationError('商品ID错误')
        else:
            self.good = good
            return good_id

    def clean(self):
        if self.good.inventory < self.clean_data.get('num'):
            raise forms.ValidationError('商品库存不足，请修改添加量')
        return self.cleaned_data

    def save(self):
        with transaction.atomic():
            num = self.cleaned_data.get('num')
            try:
                cart = CartItem.objects.get(user=self.user, good=self.good)
            except Exception as e:
                print e
                cart = CartItem.objects.create(user=self.user, good=self.good, num=num, join_price=self.good.sale_price)
            else:
                cart.num += num
                cart.change_time = datetime.now()
            finally:
                self.good.inventory -= num
                cart.save()
                self.good.save()


class UpdateCartItemNumForm(forms.Form):

    cart_id = forms.IntegerField(required=True, error_messages={
        'required': '购物车子项ID不能为空',
    })
    num = forms.IntegerField(required=True, error_messages={
        'required': '修改内容不能为空',
    })


    def clean_car_id(self):
        pass

class CreateOrderForm(forms.Form):

    community_id = forms.CharField(required=True, error_messages={
        'required': '所属社区不能为空',
    })

    def save(self):
        community_id = self.cleaned_data('community_id')
        code = datetime.now().strftime('%Y%m%d%H%M%S')+uuid.uuid1()






