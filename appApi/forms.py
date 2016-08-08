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
    account = forms.CharField(max_length=20, required=True,
                              error_messages={
                                  'required': u'请输入正确手机号',
                                  'max_length': u'请输入正确手机号',
                              })
    code = forms.CharField(min_length=6,max_length=6,required=True,
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

    def clean(self):
        account = self.cleaned_data.get('account', None);
        pswd = self.cleaned_data.get('pswd', None)

        if account and pswd:
            try:
                exit_user = User.objects.get(phone=account)
                if exit_user is None:
                    return self.cleaned_data
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_register'])
            except Exception as err:
                print(err)
        else:
            raise forms.ValidationError(
                self.error_messages['invalid_register'])

    def save(self):
        account = self.cleaned_data.get('account', None);
        code = self.cleaned_data['code']
        pswd = self.cleaned_data['pswd']
        user = User(phone=account, pswd=pswd)
        user.save();




