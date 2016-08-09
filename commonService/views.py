#coding:utf-8
from functools import wraps

from django.http.response import HttpResponse, JsonResponse


HASH_SESSION_KEY = '_auth_user_hash'
SESSION_KEY = '_auth_user_id'
class AjaxResponseMixin(object):

    status = 'success'
    error_messages = 'message'

    def update_errors(self, msg, errors=None):
        self.status = 'error'
        if errors is not None:
            self.error_messages = errors
        else:
            self.error_messages = msg

    def render_to_json(self, data):
        context = {
            'status': self.status,
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