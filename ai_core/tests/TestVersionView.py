import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.core.views import VersionView
from apps.users.profile.models import UserProfile
from tests.utils.backends import FIXTURES_FOLDER_PATH, force_authenticate


class TestVersionView(TestCase):
    fixtures = [os.path.join(FIXTURES_FOLDER_PATH, 'test-data.json')]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = VersionView.as_view()

        self.auth_user = UserProfile.objects.get(id=1)

    def test_view_can_get_version(self):
        request = self.factory.get(reverse('version'))
        request.language = 'en'
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('version'), settings.VERSION)

    def test_view_can_get_authenticated_version(self):
        request = self.factory.get(reverse('version'))
        request.language = 'en'
        force_authenticate(request, self.auth_user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('version'), settings.VERSION)
