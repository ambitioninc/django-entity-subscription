from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from entity import Entity, EntityRelationship


class SubscriptionManager(models.Manager):
    def mediums_subscribed(self, source, entity, subentity_type=None):
        if subentity_type is None:
            return self._mediums_subscribed_individual(source, entity)
        else:
            return self._mediums_subscribed_group(source, entity, subentity_type)

    def is_subscribed(self, source, medium, entity, subentity_type=None):
        if subentity_type is None:
            return self._is_subscribed_individual(source, mediusm, entity)
        else:
            return self._is_subscribed_group(source, medium, entity, subentity_type)

    def _mediums_subscribed_individual(self, source, entity):
        super_entities = entity.get_super_entities()
        entity_is_subscribed = Q(subentity_type__isnull=True, entity=entity)
        super_entity_is_subscribed = Q(subentity_type=entity.entity_type, entity__in=super_entities)
        subscribed_mediums = set(
            self
            .filter(entity_is_subscribed | super_entity_is_subscribed, source=source)
            .select_related('medium')
            .values_list('medium', flat=True)
        )
        unsubscribed_mediums = set(
            Unsubscribe.objects
            .filter(entity=entity, source=source)
            .select_related('medium')
            .values_list('medium', flat=True)
        )
        return Medium.objects.filter(id__in=subscribed_mediums - unsubscribed_mediums)

    def _mediums_subscribed_group(self, source, entity, subentity_type):
        # For every subentity, if that subentity is part of a
        # subscription, include the medium for that subscription.
        related_super_entities = EntityRelationship.objects.filter(
            sub_entity__in=entity.get_sub_entities().is_type(subentity_type)
        ).values_list('super_entity')
        group_subscribed_mediums = set(
            self
            .filter(source=source, subentity_type=subentity_type, entity__in=related_super_entities)
            .select_related('medium')
            .values_list('medium', flat=True)
        )
        return Medium.objects.filter(id__in=group_subscribed_mediums)


    def _is_subscribed_individual(self, source, medium, entity):
        pass

    def _is_subscribed_group(self, source, medium, entity, subentity_type):
        pass


class Subscription(models.Model):
    """Include groups of entities to subscriptions.

    It is recommended that these be largely pre-configured within an
    application, as catch-all groups. The finer grained control of
    individual users subscription status is defined within the
    `Unsubscribe` model.

    If, however, you want to subscribe an individual entity to a
    source/medium combination, setting the `subentity_type` field to
    None will create an individual subscription.
    """
    medium = models.ForeignKey('Medium')
    source = models.ForeignKey('Source')
    entity = models.ForeignKey(Entity)
    subentity_type = models.ForeignKey(ContentType, null=True)

    objects = SubscriptionManager()


class Unsubscribe(models.Model):
    """Individual entity-level unsubscriptions.

    Entities can opt-out individually from recieving any notification
    of a given source/medium combination.
    """
    entity = models.ForeignKey(Entity)
    medium = models.ForeignKey('Medium')
    source = models.ForeignKey('Source')


class Medium(models.Model):
    """A method of actually delivering the notification to users.

    Mediums describe a particular method the application has of
    sending notifications. The code that handles actually sending the
    message should own a medium object that represents itself, or at
    least, know the name of one.
    """
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()


class Source(models.Model):
    """A category of where notifications originate from.

    Sources should make sense as a category of notifications to users,
    and pieces of the application which create that type of
    notification should own a `source` object which they can pass
    along to the business logic for distributing the notificaiton.
    """
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()
