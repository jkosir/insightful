from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from django.test import TestCase

from core.mixins import ChartsUtilityMixin
from core.views import AngularView


class CoreTestCase(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.factory = RequestFactory()

    def test_loginrequired_mixin(self):
        request = self.factory.get(reverse('app', args=[2, ]))
        request.user = AnonymousUser()
        response = AngularView.as_view()(request)
        self.assertEqual(response.url, reverse('accounts:login') + '?next=' + reverse('app', args=[2, ]))

    def test_charts_mixin(self):
        mixin = ChartsUtilityMixin()
        mixin.kwargs = {'website_id': 1}
        for pageview in mixin.pageviews:
            self.assertEqual(pageview.session.website_id, 1)






