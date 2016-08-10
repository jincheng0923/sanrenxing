# coding:utf-8

from django import forms
from django.contrib.auth import authenticate
from models import User

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
        mobilecode = self.changed_data.get('mobilecode')
        print u'----------'+mobilecode
        if code != mobilecode :
            raise forms.ValidationError(
                self.error_messages['invalid_code_error'])

    def clean(self):
        phone = self.cleaned_data.get('phone', None);
        pswd = self.cleaned_data.get('pswd', None)

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
        user = User(phone=account, pswd=pswd)
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





