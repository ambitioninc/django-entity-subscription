from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from entity_subscription import admin
from entity_subscription.models import Medium, Source, Subscription, Unsubscribe


class AdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_all_can_be_called(self):
        admin.MediumAdmin(Medium, self.site)
        admin.SourceAdmin(Source, self.site)
        admin.SubscriptionAdmin(Subscription, self.site)
        admin.UnsubscribeAdmin(Unsubscribe, self.site)
