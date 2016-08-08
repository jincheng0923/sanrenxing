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