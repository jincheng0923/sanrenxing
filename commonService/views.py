#coding:utf-8
from functools import wraps
import re

from django.http.response import HttpResponse, JsonResponse
import requests


HASH_SESSION_KEY = '_auth_user_hash'
SESSION_KEY = '_auth_user_id'
class AjaxResponseMixin(object):

    status = 'true'
    error_messages = 'message'

    def update_errors(self, msg, errors=None):
        self.status = 'false'
        if errors is not None:
            self.error_messages = errors
        else:
            self.error_messages = msg

    def render_to_json(self, data):
        context = {
            'success': self.status,
            'msg': self.error_messages,
        }
        context.update(data)
        return JsonResponse(context)

    def ajax_response(self, context=None, **kwargs):
        if context is None:
            context = {}
        if not isinstance(context, dict):
            context = {'data': context}
        context.update(**kwargs)

        return self.render_to_json(context)


from appApi.models import User
from appApi.models import Smsmessage

class MyCustomBackend(object):

    def authenticate(self, phone=None, password=None):
        if phone.check_password(password):
            return phone
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def ajax_login_required(func):
    ''' Verify the user when ajax request wheather he is login.'''
    @wraps(func)
    def verify_login(request, *args, **kwargs):
        if request.session[HASH_SESSION_KEY]:
            print request.session[HASH_SESSION_KEY]
            return func(request, *args, **kwargs)
        else:
            to_return = {
                'result': 'error',
                'msg': u'账号没有登陆'
            }
            return JsonResponse(to_return)
    return verify_login


def send_sms(phone, content, source=None):

    url = 'http://120.25.147.10:8002/sms.aspx'
    params = {
        'userid': 843,
        'account': 'SEE',
        'password': '456789',
        'mobile': phone,
        'content': content,
        'sendTime': '',
        'action': 'send',
        'extno': ''
    }

    req = requests.get(url, params)
    if req.status_code == 200:
        pattern = re.compile(r'Success55')
        match = pattern.search(req.content)
        if match:
            sm = Smsmessage.objects.create(phone=phone, content=content, status='S', source=source)
            return True
        else:
            sm = Smsmessage.objects.create(phone=phone, content=content, status='F', source=source)
            return False
    else:
        sm = Smsmessage.objects.create(phone=phone, content=content, status='F', source=source)
        return False

