from django.http import HttpResponseRedirect
from sessions import SESSION_KEY


def require_session():
    def decorator(func):
        def wrapped(request, *args, **kwargs):
            if request.session.has_key(SESSION_KEY):
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/index")
        return wrapped
    return decorator