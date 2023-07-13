import logging
from itertools import groupby

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone, translation

logger = logging.getLogger(__name__)


def get_model(model_name):
    """
    :param model_name: string matching existing model name
    :return: Model
    """
    _apps = list(map(lambda x: x.split(".")[-1], settings.INSTALLED_APPS))  # Gets the last part of the app name
    app_label = ContentType.objects.get(app_label__in=_apps, model__iexact=model_name).app_label
    return apps.get_model(app_label=app_label, model_name=model_name)


def get_language(language=None):
    """
    :param language: string to convert in a language
    :return: Language code in two letter format 'en'
    """
    if not language:
        language = translation.get_language()
    return translation.to_locale(language).split("_")[0].lower()


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


def today(d=None):
    """
    :param d: datetime
    :return: Tuple containing (year, month, week, day, date)
    """
    if not d:
        d = timezone.now()
    return d.year, d.month, d.isocalendar()[1], d.day, d.date()


def queryset_to_keyed_dict(queryset, serializer, key_function):
    """
    Converts a queryset to a dict using the field selected with "key_function" as key
    :param queryset: Django queryset
    :param serializer: Used to serialize dictionary value
    :param key_function: Function used to select key field. Ex: lambda q: q.key
    :return: {key: serialized_value}
    """
    return {k.lower(): serializer(g, many=True).data for k, g in groupby(queryset, key=key_function)}
