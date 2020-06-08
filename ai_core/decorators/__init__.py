from django.conf import settings
from rest_framework.exceptions import MethodNotAllowed


def debug_only():
    """
    A decorator that wraps the passed in function and raises an exception if debug is not active
    """

    def decorator(func):

        def wrapper(*args, **kwargs):
            if not settings.DEBUG:
                raise MethodNotAllowed('Method can only be called in DEBUG=True environment.')
            return func(*args, **kwargs)

        return wrapper

    return decorator
