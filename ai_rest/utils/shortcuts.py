from django.shortcuts import _get_queryset
from django.utils.translation import gettext as _
from rest_framework import status

from ai_django.ai_rest.utils.exceptions import NotFound


def get_object_or_raise(klass, *args, label=None, **kwargs):
    """
    Uses get() to return an object, or raise NotFound if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    raised exception uses 'label' or 'id' kwargs to fill message.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """

    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_raise() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise NotFound(model=_(klass__name.lower()), value=kwargs.pop(label, kwargs.pop('id', '')))


def is_payment_required(response):
    """
    :param response: Response
    :return: Check if the error means a payment is required
    """
    return response.status_code == status.HTTP_402_PAYMENT_REQUIRED
