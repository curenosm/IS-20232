import functools
import time

from django.conf import settings
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from socks import method


def group_required(*group_names):
    """
    Requires user membership in at least one of the groups passed in.
    """
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


def anonymous_required(function=None, redirect_url=None):
    """
    Opposite of login_required
    """
    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def superuser_only(function):
    """
    Limit view to superusers only.
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return wrapper


def ajax_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return function(request, *args, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


def timeit(function):
    """
    This is util to time it takes to a function to execute
    """
    def timed(*args, **kwargs):
        ts = time.time()
        result = function(*args, **kwargs)
        te = time.time()
        print(f'{method.__name__} ({args}, {kwargs}) {te - ts:2.2f} sec')
        return result

    return timed


# Util to know this
def user_can_write_a_review(function):
    """
    Notice this is for the new docstring not to subtitute
    the original one from the function wrapped.
    """

    @functools.wraps(function)
    def wrapper(request, *args, **kwargs):
        """Extra functionality"""
        return function(request, *args, **kwargs)

    return wrapper
