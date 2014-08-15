import datetime
from django.contrib.contenttypes import generic

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.module_loading import import_by_path
from entity import Entity, EntityRelationship
import jsonfield


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
    render_class_path = models.CharField(max_length=128, null=True)

    @property
    def default_render_class_path(self):
        return 'entity_subscription.base.BaseMedium'

    def get_render_class_path(self):
        return self.render_class_path if self.render_class_path else self.default_render_class_path

    def render(self, notifications, html=True):
        medium_class = import_by_path(self.get_render_class_path())(self)
        return medium_class.render(notifications, html=html)

    def __unicode__(self):
        return self.display_name


class Action(models.Model):
    """A category of where notifications originate from.

    Actions should make sense as a category of notifications to users,
    and pieces of the application which create that type of
    notification should own an `action` object which they can pass
    along to the business logic for distributing the notificaiton.
    """
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()
    render_class_path = models.CharField(max_length=128, null=True)

    @property
    def default_render_class_path(self):
        return 'entity_subscription.base.BaseAction'

    def get_render_class_path(self):
        return self.render_class_path if self.render_class_path else self.default_render_class_path

    def __unicode__(self):
        return self.display_name


class SubscriptionManager(models.Manager):
    def mediums_subscribed(self, action, entity, subentity_type=None):
        """Return all mediums subscribed to for an action.

        Args:

          action - An `Action` object. Check the mediums subscribed to,
          for this source of notifications.

          entity - An `Entity` object. The entity to check
          subscriptions for.

          subentity_type - (Optional) A content_type indicating we're
          interested in the mediums subscribed to by all sub-entities
          of the `entity` argument matching this subentity_type.

        Returns:

           A queryset of mediums the entity is subscribed to.

           If the subentity_type is None, this queryset has all
           unsubscribed mediums filtered out.

           If the subentity_type is not None, this queryset contains
           all mediums that any of the subenties might be subscribed
           to, *without* any unsubscribed mediums filtered out.

        """
        if subentity_type is None:
            return self._mediums_subscribed_individual(action, entity)
        else:
            return self._mediums_subscribed_group(action, entity, subentity_type)

    def is_subscribed(self, action, medium, entity, subentity_type=None):
        """Return True if subscribed to this medium/action combination.

        Args:

          action - An `Action` object. Check that there is a
          subscription for this action and the given medium.

          medium - A `Medium` object. Check that there is a
          subscription for this medium and the given action

          entity - An `Entity` object. The entity to check
          subscriptions for.

          subentity_type - (Optional) A content_type indicating we're
          interested in the subscriptions by all sub-entities of the
          `entity` argument matching this subentity_type.

        Returns:

           A boolean indicating if the entity is subscribed to this
           action/medium combination.

           If the subentity_type is None, this boolean takes into
           account whether the entity is unsubscribed.

           If the subentity_type is not None, this boolean indicates
           that any of the subenties might be subscribed to this
           combination of action/medium, *without* any unsubscriptions
           filtered out.

        """
        if subentity_type is None:
            return self._is_subscribed_individual(action, medium, entity)
        else:
            return self._is_subscribed_group(action, medium, entity, subentity_type)

    def filter_not_subscribed(self, action, medium, entities):
        """Return only the entities subscribed to the action and medium.

        Args:

          action - An `Action` object. Check that there is a
          subscription for this action and the given medium.

          medium - A `Medium` object. Check that there is a
          subscription for this medium and the given action

          entities - An iterable of `Entity` objects. The iterable
          will be filtered down to only those with a subscription to
          the action and medium. All entities in this iterable must be
          of the same type.

        Raises:

          ValueError - if not all entities provided are of the same
          type.

        Returns:

          A queryset of entities which are in the initially provided
          list and are subscribed to the action and medium.

        """
        entity_type_id = entities[0].entity_type_id
        if not all(e.entity_type_id == entity_type_id for e in entities):
            msg = 'All entities provided must be of the same type.'
            raise ValueError(msg)

        group_subs = self.filter(action=action, medium=medium, subentity_type_id=entity_type_id)
        group_subscribed_entities = EntityRelationship.objects.filter(
            sub_entity__in=entities, super_entity__in=group_subs.values('entity')
        ).values_list('sub_entity', flat=True)

        individual_subs = self.filter(
            action=action, medium=medium, subentity_type=None
        ).values_list('entity', flat=True)

        relevant_unsubscribes = Unsubscribe.objects.filter(
            action=action, medium=medium, entity__in=entities
        ).values_list('entity', flat=True)

        subscribed_entities = Entity.objects.filter(
            Q(pk__in=group_subscribed_entities) | Q(pk__in=individual_subs),
            id__in=[e.id for e in entities]
        ).exclude(pk__in=relevant_unsubscribes)

        return subscribed_entities

    def _mediums_subscribed_individual(self, action, entity):
        """Return the mediums a single entity is subscribed to for a action.
        """
        super_entities = entity.super_relationships.all().values_list('super_entity')
        entity_is_subscribed = Q(subentity_type__isnull=True, entity=entity)
        super_entity_is_subscribed = Q(subentity_type=entity.entity_type, entity__in=super_entities)
        subscribed_mediums = self.filter(
            entity_is_subscribed | super_entity_is_subscribed, action=action
        ).select_related('medium').values_list('medium', flat=True)
        unsubscribed_mediums = Unsubscribe.objects.filter(
            entity=entity, action=action
        ).select_related('medium').values_list('medium', flat=True)
        return Medium.objects.filter(id__in=subscribed_mediums).exclude(id__in=unsubscribed_mediums)

    def _mediums_subscribed_group(self, action, entity, subentity_type):
        """Return all the mediums any subentity in a group is subscrbed to.
        """
        all_group_sub_entities = entity.sub_relationships.select_related('sub_entity').filter(
            sub_entity__entity_type=subentity_type
        ).values_list('sub_entity')
        related_super_entities = EntityRelationship.objects.filter(
            sub_entity__in=all_group_sub_entities
        ).values_list('super_entity')
        group_subscribed_mediums = self.filter(
            action=action, subentity_type=subentity_type, entity__in=related_super_entities
        ).select_related('medium').values_list('medium', flat=True)
        return Medium.objects.filter(id__in=group_subscribed_mediums)

    def _is_subscribed_individual(self, action, medium, entity):
        """Return true if an entity is subscribed to that action/medium combo.
        """
        super_entities = entity.super_relationships.all().values_list('super_entity')
        entity_is_subscribed = Q(subentity_type__isnull=True, entity=entity)
        super_entity_is_subscribed = Q(subentity_type=entity.entity_type, entity__in=super_entities)
        is_subscribed = self.filter(
            entity_is_subscribed | super_entity_is_subscribed,
            action=action,
            medium=medium,
        ).exists()
        unsubscribed = Unsubscribe.objects.filter(
            action=action,
            medium=medium,
            entity=entity
        ).exists()
        return is_subscribed and not unsubscribed

    def _is_subscribed_group(self, action, medium, entity, subentity_type):
        """Return true if any subentity is subscribed to that action & medium.
        """
        all_group_sub_entities = entity.sub_relationships.select_related('sub_entity').filter(
            sub_entity__entity_type=subentity_type
        ).values_list('sub_entity')
        related_super_entities = EntityRelationship.objects.filter(
            sub_entity__in=all_group_sub_entities,
        ).values_list('super_entity')
        is_subscribed = self.filter(
            action=action,
            medium=medium,
            subentity_type=subentity_type,
            entity__in=related_super_entities
        ).exists()
        return is_subscribed


class Subscription(models.Model):
    """Include groups of entities to subscriptions.

    It is recommended that these be largely pre-configured within an
    application, as catch-all groups. The finer grained control of
    individual users subscription status is defined within the
    `Unsubscribe` model.

    If, however, you want to subscribe an individual entity to a
    action/medium combination, setting the `subentity_type` field to
    None will create an individual subscription.
    """
    # The entity that is subscribed
    entity = models.ForeignKey(Entity)
    subentity_type = models.ForeignKey(ContentType, null=True)

    # The entity/action/medium being subscribed to
    medium = models.ForeignKey('Medium')
    action = models.ForeignKey('Action', null=True)
    followed_entity = models.ForeignKey(Entity, related_name='+', null=True)
    followed_subentity_type = models.ForeignKey(ContentType, related_name='+', null=True)

    objects = SubscriptionManager()

    def __unicode__(self):
        s = "{entity} to {action} by {medium}"
        entity = self.entity.__unicode__()
        action = self.action.__unicode__()
        medium = self.medium.__unicode__()
        return s.format(entity=entity, action=action, medium=medium)


class UnsubscribeManager(models.Manager):
    def is_unsubscribed(self, action, medium, entity):
        """Return True if the entity is unsubscribed
        """
        return self.filter(action=action, medium=medium, entity=entity).exists()


class Unsubscribe(models.Model):
    """Individual entity-level unsubscriptions.

    Entities can opt-out individually from recieving any notification
    of a given action/medium combination.
    """
    # entity that is unsubscribing
    entity = models.ForeignKey(Entity)

    # items unsubscribing from
    followed_entity = models.ForeignKey(Entity, related_name='+', null=True)
    medium = models.ForeignKey('Medium')
    action = models.ForeignKey('Action', null=True)

    objects = UnsubscribeManager()

    def __unicode__(self):
        s = "{entity} from {action} by {medium}"
        entity = self.entity.__unicode__()
        action = self.action.__unicode__()
        medium = self.medium.__unicode__()
        return s.format(entity=entity, action=action, medium=medium)


class NotificationQuerySet(models.query.QuerySet):
    def medium(self, medium, include_seen=True):
        """Return notifications for a given medium.

        Args:

          medium - A medium object to check for.

          include_seen (Optional) - If `False`, exclude all
          notification that have already been marked as seen.

        Returns:

          A QuerySet that filters out all notifications that are not
          for the given medium. Can additionally filter out
          notifications that have already been seen.
        """
        if include_seen:
            notifications_for_medium = NotificationMedium.objects.filter(
                medium=medium,
            ).values_list('notification')
        else:
            notifications_for_medium = NotificationMedium.objects.filter(
                medium=medium,
                time_seen__isnull=True,
            ).values_list('notification')
        return self.filter(id__in=notifications_for_medium)

    def mark_seen(self, for_medium):
        """Set `time_seen` on the selected notifications for the medium.

        If there are any notifications that already have a `time_seen`
        their values will not be updated.

        Args:

          for_medium - A medium object to update `time_seen` objects
          for.

        Returns:

           The number of objects that are marked as seen.

        """
        time = datetime.datetime.utcnow()
        updated = NotificationMedium.objects.filter(
            notification__in=self,
            medium=for_medium,
            time_seen__isnull=True,
        ).update(time_seen=time)
        return updated


class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model)

    def get_subscribe_queryset(self, entity, medium):
        subscribe_filter = Q(medium=medium) & Q(entity=entity)

        if entity.__class__ is Entity:
            entities_queryset = Entity.objects.filter(sub_relationships__sub_entity=entity)
            subscribe_filter = Q(medium=medium) & Q(Q(entity=entity) | Q(entity__in=entities_queryset))

        subscribe_queryset = Subscription.objects.filter(subscribe_filter)
        return subscribe_queryset

    def get_unsubscribe_queryset(self, entity, medium):
        unsubscribe_filter = Q(medium=medium) & Q(entity=entity)
        unsubscribe_queryset = Unsubscribe.objects.filter(unsubscribe_filter)
        return unsubscribe_queryset

    def get_filters(self, subscribe_queryset):
        filters = {
            'only_entity': Q(),
            'only_action': Q(),
            'entity_action': Q(),
        }

        for subscription in subscribe_queryset:
            if subscription.followed_subentity_type:
                # We assume there is a followed_entity if there is a followed_subentity_type
                entities_queryset = Entity.objects.filter(
                    entity_type=subscription.followed_subentity_type,
                    super_relationships__super_entity=subscription.followed_entity)
                if subscription.action:
                    filters['entity_action'].add(
                        Q(actor_id__in=entities_queryset) &
                        Q(action=subscription.action),
                        Q.OR
                    )
                else:
                    filters['only_entity'].add(
                        Q(actor_id__in=entities_queryset),
                        Q.OR
                    )
            else:
                if subscription.followed_entity:
                    followed_entity_type = ContentType.objects.get_for_model(subscription.followed_entity)
                    if subscription.action:
                        filters['entity_action'].add(
                            Q(actor_id=subscription.followed_entity.id) &
                            Q(action=subscription.action),
                            Q.OR
                        )
                    else:
                        filters['only_entity'].add(
                            Q(actor_id=subscription.followed_entity.id),
                            Q.OR
                        )
                else:
                    filters['only_action'].add(Q(action=subscription.action), Q.OR)

        return filters

    def get_excludes(self, unsubscribe_queryset):
        excludes = {
            'only_entity': Q(),
            'only_action': Q(),
            'entity_action': Q(),
        }

        for unsubscribe in unsubscribe_queryset:
            if unsubscribe.followed_entity:
                followed_entity_type = ContentType.objects.get_for_model(unsubscribe.followed_entity)
                if unsubscribe.action:
                    excludes['entity_action'].add(
                        Q(actor_id=unsubscribe.followed_entity.id) &
                        Q(action=unsubscribe.action),
                        Q.OR
                    )
                else:
                    excludes['only_entity'].add(
                        Q(actor_id=unsubscribe.followed_entity.id),
                        Q.OR
                    )
            else:
                excludes['only_action'].add(Q(action=unsubscribe.action), Q.OR)

        return excludes

    def get_filtered_queryset(self, filters, excludes):
        return self.get_queryset().filter(
            filters['only_entity'] | filters['only_action'] | filters['entity_action']
        ).exclude(
            excludes['only_entity'] | excludes['only_action'] | excludes['entity_action']
        )

    def get_for_entity(self, entity, medium):
        subscribe_queryset = self.get_subscribe_queryset(entity, medium)

        if subscribe_queryset.count() == 0:
            return self.get_queryset().none()

        filters = self.get_filters(subscribe_queryset)

        unsubscribe_queryset = self.get_unsubscribe_queryset(entity, medium)
        excludes = self.get_excludes(unsubscribe_queryset)

        return self.get_filtered_queryset(filters, excludes)

    def medium(self, *args, **kwargs):
        return self.get_queryset().medium(*args, **kwargs)

    def mark_seen(self, *args, **kwargs):
        return self.get_queryset().mark_seen(*args, **kwargs)

    def create_notification(
            self, actor, action, action_object=None, target=None, context=None, expires=None, event_id=None):
        """Create notifications, if the appropriate subscription exits.

        This method also creates the appropriate NotificationMedium
        records, which identify how the notification is to be
        delivered to the user. By default, NotificationMedium records
        are created for each medium the entity is subscribed to.

        Args:

          entity - The entity to be notified.

          notification_action - An action object for the notification.

          context - A python dictionary of information describing the
          notification. This is the context that will be used to
          render the notification when it is delieverd to the user.

          mediums (Optional) - If provided, restricts notifications to
          be created for the mediums given. If there are no
          subscriptions for those mediums, no notification will be created.

          expires (Optional) - A datetime or timedelta that signifies
          when the notification is no longer relevant. It is used to
          set the `time_expires` field on the notification. If a
          timedelta is given, the `time_expires` field will be set to
          the current time plus the timedelta.

          subentity_type (Optional) - A content type. If
          subentity_type is not `None` it signifies that this is a
          notification for a group. This field then describes the type
          of sub-entity of the given entity that are in the group to
          be notified.

          event_id (Optional) - A string that uniquely identifies the
          notification. If not given, one will be created. If the event_id
          is not unique, an error will be raised.

        Returns:

          The notification object created. If no subscriptions exist
          for the notification, returns None.

        Raises:

          IntegrityError - raised if the provided event_id already exists
          in a Notification.
        """
        current_time = datetime.datetime.utcnow()
        if isinstance(expires, datetime.timedelta):
            expires = current_time + expires
        if not event_id:
            event_id = '{action}-{timestamp}'.format(
                action=action.name,
                timestamp=current_time.strftime('%Y.%d.%m.%H.%M.%S.%f')
            )

        # Get actor info
        actor_type = ContentType.objects.get_for_model(actor)
        actor_id = actor.id

        # Get action object info
        action_object_type = None
        action_object_id = None
        if action_object:
            action_object_type = ContentType.objects.get_for_model(action_object)
            action_object_id = action_object.id

        # Get target info
        target_type = None
        target_id = None
        if target:
            target_type = ContentType.objects.get_for_model(target)
            target_id = target.id

        # Create the notification
        notification = self.create(
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            action_object_type=action_object_type,
            action_object_id=action_object_id,
            target_type=target_type,
            target_id=target_id,
            context=context,
            time_expires=expires,
            event_id=event_id,
        )

        # Then we create all the related medium objects.
        # NotificationMedium.objects.bulk_create(
        #     NotificationMedium(notification=notification, medium=medium)
        #     for medium in mediums
        # )
        return notification


class Notification(models.Model):
    actor_type = models.ForeignKey(ContentType, related_name='+')
    actor_id = models.PositiveIntegerField()
    actor = generic.GenericForeignKey('actor_type', 'actor_id')

    action = models.ForeignKey(Action)

    action_object_type = models.ForeignKey(ContentType, related_name='+', null=True)
    action_object_id = models.PositiveIntegerField(null=True)
    action_object = generic.GenericForeignKey('action_object_type', 'action_object_id')

    target_type = models.ForeignKey(ContentType, related_name='+', null=True)
    target_id = models.PositiveIntegerField(null=True)
    target = generic.GenericForeignKey('target_type', 'target_id')

    context = jsonfield.JSONField()

    time_created = models.DateTimeField(auto_now_add=True)
    time_expires = models.DateTimeField(null=True, default=None)

    # used to identify a type of notification to prevent duplicates and to group similar notifications
    event_id = models.CharField(max_length=128)

    objects = NotificationManager()

    def render(self, html=True):
        action_class = import_by_path(self.action.get_render_class_path())(self)
        return action_class.render(html=html)


class NotificationMedium(models.Model):
    notification = models.ForeignKey('Notification')
    medium = models.ForeignKey(Medium)
    entity = models.ForeignKey(Entity)
    time_seen = models.DateTimeField(null=True, default=None)
