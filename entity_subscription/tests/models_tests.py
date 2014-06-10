from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django_dynamic_fixture import G
from entity.models import Entity, EntityRelationship

from entity_subscription.models import Medium, Source, Subscription, Unsubscribe


class SubscriptionManagerMediumsSubscribedIndividualTest(TestCase):
    def setUp(self):
        self.medium_1 = G(Medium)
        self.medium_2 = G(Medium)
        self.source_1 = G(Source)
        self.source_2 = G(Source)

    def test_individual_subscription(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_type=None)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        expected_medium = self.medium_1
        self.assertEqual(mediums.first(), expected_medium)

    def test_group_subscription(self):
        ct = G(ContentType)
        super_e = G(Entity)
        sub_e = G(Entity, entity_type=ct)
        G(EntityRelationship, super_entity=super_e, sub_entity=sub_e)
        G(Subscription, entity=super_e, medium=self.medium_1, source=self.source_1, subentity_type=ct)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=sub_e)
        expected_medium = self.medium_1
        self.assertEqual(mediums.first(), expected_medium)

    def test_multiple_mediums(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_type=None)
        G(Subscription, entity=entity_1, medium=self.medium_2, source=self.source_1, subentity_type=None)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        self.assertEqual(mediums.count(), 2)

    def test_unsubscribed(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_type=None)
        G(Subscription, entity=entity_1, medium=self.medium_2, source=self.source_1, subentity_type=None)
        G(Unsubscribe, entity=entity_1, medium=self.medium_1, source=self.source_1)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_2)

    def test_filters_by_source(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_type=None)
        G(Subscription, entity=entity_1, medium=self.medium_2, source=self.source_2, subentity_type=None)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        self.assertEqual(mediums.count(), 1)


class SubscriptionManagerMediumsSubscribedGroup(TestCase):
    def setUp(self):
        self.ct = G(ContentType)
        self.source_1 = G(Source)
        self.source_2 = G(Source)
        self.medium_1 = G(Medium)
        self.medium_2 = G(Medium)

    def test_one_subscription_matches_across_supers(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        sub = G(Entity, entity_type = self.ct)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_2, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_type=self.ct)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_2, self.ct)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_1)

    def test_multiple_subscriptions_match_acorss_supers(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        super_3 = G(Entity)
        sub = G(Entity, entity_type = self.ct)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_2, sub_entity=sub)
        G(EntityRelationship, super_entity=super_3, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_type=self.ct)
        G(Subscription, entity=super_2, medium=self.medium_2, source=self.source_1, subentity_type=self.ct)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_3, self.ct)
        self.assertEqual(mediums.count(), 2)

    def test_filters_by_source(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        sub = G(Entity, entity_type = self.ct)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_2, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_type=self.ct)
        G(Subscription, entity=super_1, medium=self.medium_2, source=self.source_2, subentity_type=self.ct)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_2, self.ct)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_1)

    def test_filters_by_super_entity_intersections(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        super_3 = G(Entity)
        sub = G(Entity, entity_type = self.ct)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_3, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_type=self.ct)
        G(Subscription, entity=super_2, medium=self.medium_2, source=self.source_1, subentity_type=self.ct)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_3, self.ct)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_1)
