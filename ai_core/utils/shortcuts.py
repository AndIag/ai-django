import logging
import uuid
from datetime import timedelta, datetime, date
from itertools import groupby

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import _get_queryset, get_object_or_404
from django.utils import timezone, translation
from django.utils.translation import gettext as _
from rest_framework import status

from ai_django.ai_core.utils.exceptions import NotFound

logger = logging.getLogger(__name__)


def generate_unique_code(length=8):
    """
    :return: Generated 'length' length hexadecimal number
    """
    return uuid.uuid4().hex[:length].upper()


def get_model(model_name):
    """
    :param model_name: string matching existing model name
    :return: Model
    """
    tsapps = list(map(lambda x: x.split('.')[-1], settings.TSQUAD_APPS))  # Gets the last part of the app name
    app_label = ContentType.objects.get(app_label__in=tsapps, model__iexact=model_name).app_label
    return apps.get_model(app_label=app_label, model_name=model_name)


def get_language(language=None):
    """
    :param language: string to convert in a language
    :return: Language code in two letter format 'en'
    """
    if not language:
        language = translation.get_language()
    return translation.to_locale(language).split('_')[0].lower()


def get_object_or_none(klass, *args, **kwargs):
    """
    Changes django get_object_or_404 method returning None instead of 404.
    """

    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404:
        return None


def get_object_id_or_none(klass, *args, **kwargs):
    """
    Changes django get_object_or_404 method returning None instead of 404.
    """

    try:
        return get_object_or_404(klass, *args, **kwargs).id
    except Http404:
        return None


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


def copy(d, exclude=None):
    """
    :param d: valid dictionary
    :param exclude: keys to exclude
    :return: A copy of the given dict without excluded keys
    """
    if exclude is None:
        exclude = []
    return {k: v for k, v in d.items() if k not in exclude}


def all_none(*args):
    """
    :param args: List of params to validate.
    :return: bool
    """
    return all(x is None for x in args)


def all_not_none(*args):
    """
    :param args: List of params to validate.
    :return: bool
    """
    return all(x is not None for x in args)


def all_or_none(*args):
    """
    :param args: List of params to validate.
    :return: bool
    """
    return all_none(*args) or all_not_none(*args)


def today(d=None):
    """
    :param d: datetime
    :return: Tuple containing (year, month, week, day, date)
    """
    if not d:
        d = timezone.now()
    return d.year, d.month, d.isocalendar()[1], d.day, d.date()


def week_to_date(week, year):
    """
    Return datetime for the given week, year. (https://stackoverflow.com/a/17087427)
    :param week: number
    :param year: number
    :return: datetime
    """
    ret = datetime.strptime('{}-W{}'.format(year, week) + '-1', "%Y-W%W-%w")
    if date(year, 1, 4).isoweekday() > 4:
        """
        ISO defines week one to contain January 4th so the result is off by one iff the first Monday and 4 January are 
        in different weeks. The latter is the case if 4 January is a Friday, Saturday or Sunday.
        (https://stackoverflow.com/a/5884021)
        """
        ret -= timedelta(days=7)
    return ret


def weeks_between(d1, d2):
    """
    Distance weeks between two dates. (https://stackoverflow.com/a/14191915)
    :param d1: datetime
    :param d2: datetime
    :return: timedelta
    """
    monday1 = (d1 - timedelta(days=d1.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))
    return timedelta(weeks=(monday2 - monday1).days / 7)


def is_payment_required(response):
    """
    :param response: Response
    :return: Check if the error means a payment is required
    """
    return response.status_code == status.HTTP_402_PAYMENT_REQUIRED


def queryset_to_keyed_dict(queryset, serializer, key_function):
    """
    Converts a queryset to a dict using the field selected with "key_function" as key
    :param queryset: Django queryset
    :param serializer: Used to serialize dictionary value
    :param key_function: Function used to select key field. Ex: lambda q: q.key
    :return: {key: serialized_value}
    """
    return {k.lower(): serializer(g, many=True).data for k, g in groupby(queryset, key=key_function)}
