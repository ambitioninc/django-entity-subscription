from django.contrib.contenttypes.models import ContentType
from django.db import models, Q
from entity.models import Entity


class SubscriptionManager(models.Manager):
    def mediums_subscribed(self, entity, source):
        super_entities = entity.get_super_entities()
        is_entity = Q(subentity_type__isnull=True, entity=entity)
        in_subentities = Q(subentity_type_=entity.entity_type, entity__in=super_entities)
        subscribed_mediums = set(
            self.filter(is_entity | in_subentities).values_list('medium', flat=True)
        )
        unsubscribed_mediums = set(
            Unsubscribed.objects.filter(entity=entity, source=source).values_list('medium', flat=True)
        )
        return subscribed_mediums - unsubscribed_mediums

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
