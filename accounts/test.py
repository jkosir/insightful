from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.test import TestCase
from django.contrib.messages.storage.fallback import FallbackStorage

from accounts.models import AnalyticsUser
from accounts.views import RegisterView, LoginView, AddWebsiteView
from core.models import Website


class AccountsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = AnalyticsUser.objects.create_user(email='test@test.com', password='password')

    def test_user_registration(self):
        request = self.factory.post(reverse('accounts:register'), {
            'email': 'testemail@gmail.com',
            'password1': 'passwd',
            'password2': 'passwd'
        })
        # RequestFactory doesn't support middlewares, need fallback storage for messages
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = RegisterView.as_view()(request)

        user, created = AnalyticsUser.objects.get_or_create(email='testemail@gmail.com')
        self.assertEqual(created, False)

    def test_user_login(self):
        request = self.factory.post(reverse('accounts:login'), {
            'username': 'test@test.com',
            'password': 'password'
        })
        response = LoginView.as_view()(request)
        self.assertEqual(response.url, reverse('accounts:website_list'))

    def test_website_create(self):
        request = self.factory.post(reverse('accounts:add_website'), {
            'name': 'Website name',
            'url': 'http://test.com',
            'timezone': 'Europe/Ljubljana'
        })
        request.user = self.user
        response = AddWebsiteView.as_view()(request)

        self.assertTrue(reverse('accounts:website_created') in response.url)
        self.assertEqual(Website.objects.count(), 1)

