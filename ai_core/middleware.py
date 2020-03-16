import logging

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.utils import json

logger = logging.getLogger(__name__)


class LocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        language = request.META.get('HTTP_ACCEPT_LANGUAGE', None)
        if language:
            if '-' in language:
                language = language.split('-')[0]
            if '_' in language:
                language = language.split('_')[0]
        if not language or language not in [e[0] for e in settings.LANGUAGES]:
            language = settings.LANGUAGE_CODE.split('-')[0]
        request.language = language
        translation.activate(language)

        return self.get_response(request)


class Http401TranslationMiddleware:
    """
    Adds a layer to i18n 401 errors as auth library hasn't got a method to do that
    https://django-oauth-toolkit.readthedocs.io/en/latest/
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == HTTP_401_UNAUTHORIZED:
            content = {"error": "invalid_grant", "error_description": _("Invalid credentials given.")}
            response.content = json.dumps(content)

        return response
