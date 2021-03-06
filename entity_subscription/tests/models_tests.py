from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django_dynamic_fixture import G, N
from entity.models import Entity, EntityRelationship, EntityKind
from mock import patch

from entity_subscription.models import Medium, Source, Subscription, Unsubscribe


class SubscriptionManagerMediumsSubscribedTest(TestCase):
    # We just test that this dispatches correctly. We test the
    # dispatched functions more carefully.
    @patch('entity_subscription.models.SubscriptionManager._mediums_subscribed_individual')
    def test_individual(self, subscribed_mock):
        source = N(Source)
        entity = N(Entity)
        Subscription.objects.mediums_subscribed(source, entity)
        self.assertEqual(len(subscribed_mock.mock_calls), 1)

    @patch('entity_subscription.models.SubscriptionManager._mediums_subscribed_group')
    def test_group(self, subscribed_mock):
        source = N(Source)
        entity = N(Entity)
        ct = N(ContentType)
        Subscription.objects.mediums_subscribed(source, entity, ct)
        self.assertEqual(len(subscribed_mock.mock_calls), 1)


class SubscriptionManagerIsSubscribedTest(TestCase):
    # We just test that this dispatches correctly. We test the
    # dispatched functions more carefully.
    @patch('entity_subscription.models.SubscriptionManager._is_subscribed_individual')
    def test_individual(self, subscribed_mock):
        source = N(Source)
        medium = N(Medium)
        entity = N(Entity)
        Subscription.objects.is_subscribed(source, medium, entity)
        self.assertEqual(len(subscribed_mock.mock_calls), 1)

    @patch('entity_subscription.models.SubscriptionManager._is_subscribed_group')
    def test_group(self, subscribed_mock):
        source = N(Source)
        medium = N(Medium)
        entity = N(Entity)
        ct = N(ContentType)
        Subscription.objects.is_subscribed(source, medium, entity, ct)
        self.assertEqual(len(subscribed_mock.mock_calls), 1)


class SubscriptionManagerMediumsSubscribedIndividualTest(TestCase):
    def setUp(self):
        self.medium_1 = G(Medium)
        self.medium_2 = G(Medium)
        self.source_1 = G(Source)
        self.source_2 = G(Source)

    def test_individual_subscription(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_kind=None)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        expected_medium = self.medium_1
        self.assertEqual(mediums.first(), expected_medium)

    def test_group_subscription(self):
        ek = G(EntityKind)
        super_e = G(Entity)
        sub_e = G(Entity, entity_kind=ek)
        G(EntityRelationship, super_entity=super_e, sub_entity=sub_e)
        G(Subscription, entity=super_e, medium=self.medium_1, source=self.source_1, subentity_kind=ek)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=sub_e)
        expected_medium = self.medium_1
        self.assertEqual(mediums.first(), expected_medium)

    def test_multiple_mediums(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_kind=None)
        G(Subscription, entity=entity_1, medium=self.medium_2, source=self.source_1, subentity_kind=None)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        self.assertEqual(mediums.count(), 2)

    def test_unsubscribed(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_kind=None)
        G(Subscription, entity=entity_1, medium=self.medium_2, source=self.source_1, subentity_kind=None)
        G(Unsubscribe, entity=entity_1, medium=self.medium_1, source=self.source_1)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_2)

    def test_filters_by_source(self):
        entity_1 = G(Entity)
        G(Subscription, entity=entity_1, medium=self.medium_1, source=self.source_1, subentity_kind=None)
        G(Subscription, entity=entity_1, medium=self.medium_2, source=self.source_2, subentity_kind=None)
        mediums = Subscription.objects._mediums_subscribed_individual(source=self.source_1, entity=entity_1)
        self.assertEqual(mediums.count(), 1)


class SubscriptionManagerMediumsSubscribedGroup(TestCase):
    def setUp(self):
        self.ek = G(EntityKind)
        self.source_1 = G(Source)
        self.source_2 = G(Source)
        self.medium_1 = G(Medium)
        self.medium_2 = G(Medium)

    def test_one_subscription_matches_across_supers(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        sub = G(Entity, entity_kind=self.ek)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_2, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_2, self.ek)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_1)

    def test_multiple_subscriptions_match_acorss_supers(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        super_3 = G(Entity)
        sub = G(Entity, entity_kind=self.ek)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_2, sub_entity=sub)
        G(EntityRelationship, super_entity=super_3, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek)
        G(Subscription, entity=super_2, medium=self.medium_2, source=self.source_1, subentity_kind=self.ek)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_3, self.ek)
        self.assertEqual(mediums.count(), 2)

    def test_filters_by_source(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        sub = G(Entity, entity_kind=self.ek)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_2, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek)
        G(Subscription, entity=super_1, medium=self.medium_2, source=self.source_2, subentity_kind=self.ek)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_2, self.ek)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_1)

    def test_filters_by_super_entity_intersections(self):
        super_1 = G(Entity)
        super_2 = G(Entity)
        super_3 = G(Entity)
        sub = G(Entity, entity_kind=self.ek)
        G(EntityRelationship, super_entity=super_1, sub_entity=sub)
        G(EntityRelationship, super_entity=super_3, sub_entity=sub)
        G(Subscription, entity=super_1, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek)
        G(Subscription, entity=super_2, medium=self.medium_2, source=self.source_1, subentity_kind=self.ek)
        mediums = Subscription.objects._mediums_subscribed_group(self.source_1, super_3, self.ek)
        self.assertEqual(mediums.count(), 1)
        self.assertEqual(mediums.first(), self.medium_1)


class SubscriptionManagerIsSubScribedIndividualTest(TestCase):
    def setUp(self):
        self.ek = G(EntityKind)
        self.medium_1 = G(Medium)
        self.medium_2 = G(Medium)
        self.source_1 = G(Source)
        self.source_2 = G(Source)
        self.entity_1 = G(Entity, entity_kind=self.ek)
        self.entity_2 = G(Entity)
        G(EntityRelationship, sub_entity=self.entity_1, super_entity=self.entity_2)

    def test_is_subscribed_direct_subscription(self):
        G(Subscription, entity=self.entity_1, medium=self.medium_1, source=self.source_1, subentity_kind=None)
        is_subscribed = Subscription.objects._is_subscribed_individual(
            self.source_1, self.medium_1, self.entity_1
        )
        self.assertTrue(is_subscribed)

    def test_is_subscribed_group_subscription(self):
        G(Subscription, entity=self.entity_2, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek)
        is_subscribed = Subscription.objects._is_subscribed_individual(
            self.source_1, self.medium_1, self.entity_1
        )
        self.assertTrue(is_subscribed)

    def test_filters_source(self):
        G(Subscription, entity=self.entity_1, medium=self.medium_1, source=self.source_2, subentity_kind=None)
        is_subscribed = Subscription.objects._is_subscribed_individual(
            self.source_1, self.medium_1, self.entity_1
        )
        self.assertFalse(is_subscribed)

    def test_filters_medium(self):
        G(Subscription, entity=self.entity_1, medium=self.medium_2, source=self.source_1, subentity_kind=None)
        is_subscribed = Subscription.objects._is_subscribed_individual(
            self.source_1, self.medium_1, self.entity_1
        )
        self.assertFalse(is_subscribed)

    def test_super_entity_means_not_subscribed(self):
        G(Subscription, entity=self.entity_1, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek)
        is_subscribed = Subscription.objects._is_subscribed_individual(
            self.source_1, self.medium_1, self.entity_1
        )
        self.assertFalse(is_subscribed)

    def test_not_subscribed(self):
        is_subscribed = Subscription.objects._is_subscribed_individual(
            self.source_1, self.medium_1, self.entity_1
        )
        self.assertFalse(is_subscribed)

    def test_unsubscribed(self):
        G(Subscription, entity=self.entity_1, medium=self.medium_1, source=self.source_1, subentity_kind=None)
        G(Unsubscribe, entity=self.entity_1, medium=self.medium_1, source=self.source_1)
        is_subscribed = Subscription.objects._is_subscribed_individual(
            self.source_1, self.medium_1, self.entity_1
        )
        self.assertFalse(is_subscribed)


class SubscriptionManagerIsSubscribedGroupTest(TestCase):
    def setUp(self):
        self.ek_1 = G(EntityKind)
        self.ek_2 = G(EntityKind)
        self.medium_1 = G(Medium)
        self.medium_2 = G(Medium)
        self.source_1 = G(Source)
        self.source_2 = G(Source)
        self.entity_1 = G(Entity, entity_kind=self.ek_1)    # sub
        self.entity_2 = G(Entity)                           # super
        self.entity_3 = G(Entity)                           # super
        self.entity_4 = G(Entity, entity_kind=self.ek_2)    # sub
        G(EntityRelationship, sub_entity=self.entity_1, super_entity=self.entity_2)
        G(EntityRelationship, sub_entity=self.entity_1, super_entity=self.entity_3)
        G(EntityRelationship, sub_entity=self.entity_4, super_entity=self.entity_2)
        G(EntityRelationship, sub_entity=self.entity_4, super_entity=self.entity_3)

    def test_one_subscription_matches_across_supers(self):
        G(Subscription, entity=self.entity_2, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek_1)
        is_subscribed = Subscription.objects._is_subscribed_group(
            source=self.source_1, medium=self.medium_1, entity=self.entity_3, subentity_kind=self.ek_1
        )
        self.assertTrue(is_subscribed)

    def test_filters_source(self):
        G(Subscription, entity=self.entity_2, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek_1)
        is_subscribed = Subscription.objects._is_subscribed_group(
            source=self.source_2, medium=self.medium_1, entity=self.entity_3, subentity_kind=self.ek_1
        )
        self.assertFalse(is_subscribed)

    def test_filters_medium(self):
        G(Subscription, entity=self.entity_2, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek_1)
        is_subscribed = Subscription.objects._is_subscribed_group(
            source=self.source_1, medium=self.medium_2, entity=self.entity_3, subentity_kind=self.ek_1
        )
        self.assertFalse(is_subscribed)

    def test_filters_subentity_kind(self):
        G(Subscription, entity=self.entity_2, medium=self.medium_1, source=self.source_1, subentity_kind=self.ek_1)
        is_subscribed = Subscription.objects._is_subscribed_group(
            source=self.source_1, medium=self.medium_1, entity=self.entity_3, subentity_kind=self.ek_2
        )
        self.assertFalse(is_subscribed)


class SubscriptionFilterNotSubscribedTest(TestCase):
    def setUp(self):
        self.super_ek = G(EntityKind)
        self.sub_ek = G(EntityKind)
        self.super_e1 = G(Entity, entity_kind=self.super_ek)
        self.super_e2 = G(Entity, entity_kind=self.super_ek)
        self.sub_e1 = G(Entity, entity_kind=self.sub_ek)
        self.sub_e2 = G(Entity, entity_kind=self.sub_ek)
        self.sub_e3 = G(Entity, entity_kind=self.sub_ek)
        self.sub_e4 = G(Entity, entity_kind=self.sub_ek)
        self.ind_e1 = G(Entity, entity_kind=self.sub_ek)
        self.ind_e2 = G(Entity, entity_kind=self.sub_ek)
        self.medium = G(Medium)
        self.source = G(Source)
        G(EntityRelationship, sub_entity=self.sub_e1, super_entity=self.super_e1)
        G(EntityRelationship, sub_entity=self.sub_e2, super_entity=self.super_e1)
        G(EntityRelationship, sub_entity=self.sub_e3, super_entity=self.super_e2)
        G(EntityRelationship, sub_entity=self.sub_e4, super_entity=self.super_e2)

    def test_group_and_individual_subscription(self):
        G(Subscription, entity=self.ind_e1, source=self.source, medium=self.medium, subentity_kind=None)
        G(Subscription, entity=self.super_e1, source=self.source, medium=self.medium, subentity_kind=self.sub_ek)
        entities = [self.sub_e1, self.sub_e3, self.ind_e1, self.ind_e2]
        filtered_entities = Subscription.objects.filter_not_subscribed(self.source, self.medium, entities)
        expected_entity_ids = [self.sub_e1.id, self.ind_e1.id]
        self.assertEqual(set(filtered_entities.values_list('id', flat=True)), set(expected_entity_ids))

    def test_unsubscribe_filtered_out(self):
        G(Subscription, entity=self.ind_e1, source=self.source, medium=self.medium, subentity_kind=None)
        G(Subscription, entity=self.super_e1, source=self.source, medium=self.medium, subentity_kind=self.sub_ek)
        G(Unsubscribe, entity=self.sub_e1, source=self.source, medium=self.medium)
        entities = [self.sub_e1, self.sub_e2, self.sub_e3, self.ind_e1, self.ind_e2]
        filtered_entities = Subscription.objects.filter_not_subscribed(self.source, self.medium, entities)
        expected_entity_ids = [self.sub_e2.id, self.ind_e1.id]
        self.assertEqual(set(filtered_entities.values_list('id', flat=True)), set(expected_entity_ids))

    def test_entities_not_passed_in_filtered(self):
        G(Subscription, entity=self.ind_e1, source=self.source, medium=self.medium, subentity_kind=None)
        G(Subscription, entity=self.super_e1, source=self.source, medium=self.medium, subentity_kind=self.sub_ek)
        entities = [se for se in self.super_e1.get_sub_entities() if se.entity_kind == self.sub_ek]
        filtered_entities = Subscription.objects.filter_not_subscribed(self.source, self.medium, entities)
        self.assertEqual(set(filtered_entities), set(entities))

    def test_different_entity_kinds_raises_error(self):
        entities = [self.sub_e1, self.super_e1]
        with self.assertRaises(ValueError):
            Subscription.objects.filter_not_subscribed(self.source, self.medium, entities)


class UnsubscribeManagerIsUnsubscribed(TestCase):
    def test_is_unsubscribed(self):
        entity, source, medium = G(Entity), G(Source), G(Medium)
        G(Unsubscribe, entity=entity, source=source, medium=medium)
        is_unsubscribed = Unsubscribe.objects.is_unsubscribed(source, medium, entity)
        self.assertTrue(is_unsubscribed)

    def test_is_not_unsubscribed(self):
        entity, source, medium = G(Entity), G(Source), G(Medium)
        is_unsubscribed = Unsubscribe.objects.is_unsubscribed(source, medium, entity)
        self.assertFalse(is_unsubscribed)


class NumberOfQueriesTests(TestCase):
    def test_query_count(self):
        ek = G(EntityKind)
        e0 = G(Entity, entity_kind=ek)   # sub
        e1 = G(Entity, entity_kind=ek)   # sub
        e2 = G(Entity)                   # super
        e3 = G(Entity)                   # super
        e4 = G(Entity)                   # super
        e5 = G(Entity)                   # super
        e6 = G(Entity)                   # super
        m1, m2, m3, m4, m5 = G(Medium), G(Medium), G(Medium), G(Medium), G(Medium)
        s1, s2 = G(Source), G(Source)
        G(EntityRelationship, sub_entity=e1, super_entity=e2, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e1, super_entity=e3, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e1, super_entity=e4, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e1, super_entity=e5, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e1, super_entity=e6, subentity_kind=ek)

        G(EntityRelationship, sub_entity=e0, super_entity=e2, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e0, super_entity=e3, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e0, super_entity=e4, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e0, super_entity=e5, subentity_kind=ek)
        G(EntityRelationship, sub_entity=e0, super_entity=e6, subentity_kind=ek)

        G(Subscription, entity=e2, subentity_kind=ek, source=s1, medium=m1)
        G(Subscription, entity=e3, subentity_kind=ek, source=s1, medium=m2)
        G(Subscription, entity=e4, subentity_kind=ek, source=s1, medium=m3)
        G(Subscription, entity=e5, subentity_kind=ek, source=s1, medium=m4)
        G(Subscription, entity=e6, subentity_kind=ek, source=s1, medium=m5)

        G(Subscription, entity=e2, subentity_kind=ek, source=s2, medium=m1)
        G(Subscription, entity=e3, subentity_kind=ek, source=s2, medium=m2)
        G(Subscription, entity=e4, subentity_kind=ek, source=s2, medium=m3)
        G(Subscription, entity=e5, subentity_kind=ek, source=s2, medium=m4)
        G(Subscription, entity=e6, subentity_kind=ek, source=s2, medium=m5)

        with self.assertNumQueries(1):
            mediums = Subscription.objects._mediums_subscribed_individual(source=s1, entity=e1)
            list(mediums)

        with self.assertNumQueries(1):
            mediums = Subscription.objects._mediums_subscribed_group(source=s1, entity=e6, subentity_kind=ek)
            list(mediums)

        with self.assertNumQueries(2):
            Subscription.objects._is_subscribed_individual(source=s1, medium=m1, entity=e1)

        with self.assertNumQueries(1):
            Subscription.objects._is_subscribed_group(source=s1, medium=m1, entity=e6, subentity_kind=ek)

        with self.assertNumQueries(1):
            entities = [e0, e1]
            list(Subscription.objects.filter_not_subscribed(source=s1, medium=m1, entities=entities))


class UnicodeMethodTests(TestCase):
    def setUp(self):
        self.entity = G(
            Entity, entity_meta={'name': 'Entity Test'}, display_name='Entity Test'
        )
        self.medium = G(
            Medium, name='test', display_name='Test', description='A test medium.'
        )
        self.source = G(
            Source, name='test', display_name='Test', description='A test source.'
        )

    def test_subscription_unicode(self):
        sub = G(Subscription, entity=self.entity, medium=self.medium, source=self.source)
        expected_unicode = 'Entity Test to Test by Test'
        self.assertEqual(sub.__unicode__(), expected_unicode)

    def test_unsubscribe_unicode(self):
        unsub = G(Unsubscribe, entity=self.entity, medium=self.medium, source=self.source)
        expected_unicode = 'Entity Test from Test by Test'
        self.assertEqual(unsub.__unicode__(), expected_unicode)

    def test_medium_unicode(self):
        expected_unicode = 'Test'
        self.assertEqual(self.medium.__unicode__(), expected_unicode)

    def test_source_unicode(self):
        expected_unicode = 'Test'
        self.assertEqual(self.source.__unicode__(), expected_unicode)
