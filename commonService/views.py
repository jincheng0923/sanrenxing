from django.http.response import HttpResponse, JsonResponse

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

class MyCustomBackend:

    def authenticate(self, phone=None, password=None):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None