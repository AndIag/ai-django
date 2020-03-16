from django.test import TestCase
from mock import Mock

from ai_django.ai_core.middleware import LocaleMiddleware


class TestLocaleMiddleware(TestCase):
    def setUp(self):
        self.request = Mock()
        self.request.path = '/testURL/'
        self.request.session = {}
        self.middleware = LocaleMiddleware(self.request)

    def test_request_has_language(self):
        self.request.META = {"HTTP_ACCEPT_LANGUAGE": "es-Es"}
        self.middleware(self.request)
        self.assertIsNotNone(self.request.language)
        self.assertEqual(self.request.language, "es")

    def test_request_has_language_locale(self):
        self.request.META = {"HTTP_ACCEPT_LANGUAGE": "es_ES"}
        self.middleware(self.request)
        self.assertIsNotNone(self.request.language)
        self.assertEqual(self.request.language, "es")

    def test_request_has_default_language(self):
        self.request.META = {}
        self.middleware(self.request)
        self.assertIsNotNone(self.request.language)
        self.assertEqual(self.request.language, "en")
