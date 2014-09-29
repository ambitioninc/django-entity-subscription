Django Entity Subscription
==================================================

Django Entity Subscription uses the power of the `Django-Entity`_
framework to make managing subscriptions easy and powerful, for you
and your users.

.. _`Django-Entity`: https://github.com/ambitioninc/django-entity


Overview
--------------------------------------------------

This django app, includes four models:

- ``Subscription``
- ``Unsubscribe``
- ``Medium``
- ``Source``

all available from within the package ``entity_subscription.models``.

By creating objects in these models, you and the users of your
application can have fine grained control over how users are notified
and about what they are notified. The ``entity_subscription`` app is
agnostic about how users are actually notified about the subscriptions
that are set up, but is designed to be a dependency of whatever
notification system is put in place. It is assumed that the consumer
of this library already has some idea of what notifications are going
to be sent, and what delivery methods are going to be used to send the
notifications.

Once subscription information is stored in those models, the
``entity_subscription`` app also provides some methods to make it
easier to reason about and act on the stored subscriptions.

- ``Subscription.objects.mediums_subscribed``
- ``Subscription.objects.is_subscribed``

Sources and Mediums
--------------------------------------------------

The ``entity_subscription`` app creates a strong boundary between the
"source" of notifications from within an application and the "medium"
used to deliver the notification to the users of the application.


Sources
``````````````````````````````````````````````````
From a user of your application's perspective a "source" is a category
of notifications that they can subscribe to, or unsubscribe from. It
could be something like "New Products" or "Important Site
Changes".

For any given source, users may want to receive notifications over
different mediums (like "Email", "In-site", "text-message"). By
dividing notifications into different sources, users can choose to
receive that type of notification over whatever medium they prefer.

To achieve this within an application a "source" of notifications is
an object that describes where in the app a notification came
from. Pieces of code that originate events which lead to notifications
will want to own a ``Source`` object, or at least know the name of one,
so that they can clearly communicate the ``source`` of the
notifications they are originating.

The actual source objects in the database are fairly simple, and are
created through the standard ``objects.create`` interface. They have a
unique identifier, a user friendly display name, and a longer form
description.

.. code:: Python

    from entity_subscription.models import Source

    Source.objects.create(
        name='new_products',
        display_name='New Products',
        description='Tells you whenever a new item is available in the store.'
    )


Mediums
``````````````````````````````````````````````````

From a user of your application's perspective a "medium" is a way in
which they can be notified. Your site may support a variety of
different mediums for notifying your users of different
happenings. Examples could include Email, Text Messages, a News-Feed,
or a In-site Notification center.

Users will likely want to receive notifications through some
combination of the available mediums, but only for certain categories
of notifications. They may want some notifications that they view as
somewhat important to go to their email, notifications that are very
important to go to email and text-message, and all the rest to go to
an in-site notification center. By distinguishing between mediums in a
subscription library, users can decide how each "source" of
notifications is delivered to them.

The pieces of the application that handle actually sending
notifications will want to own a ``Medium`` object that describes
them, or at least know the unique name of one. This enables the code
sending notifications to handle subscriptions appropriately.

As with sources, The actual medium objects in the database are fairly
simple, and are created through the standard ``objects.create``
interface. They have a unique identifier, a user friendly display
name, and a longer form description.

.. code:: Python

    from entity_subscription.models import Medium

    Medium.objects.create(
        name='in_site',
        display_name='In Site',
        description='Notifications available in the Accounts/Notifications tab.'
    )


Source and Medium Considerations
``````````````````````````````````````````````````

Both ``Source`` and ``Medium`` objects can be effectively used as
static records that are setup as initial data for an application, or
as dynamic records that change as the various sources and mediums for
notification change. It is important to consider, however, that
excessively dynamic sources and mediums will make it difficult for
individual entities to control their subscriptions.


Subscriptions and Unsubscribing
--------------------------------------------------

Entities and groups of entities can be subscribed to
notifications. Once subscribed, individuals, mirrored as entities, can
choose to unsubscribe from notifications for a given source and
medium.


Subscriptions
``````````````````````````````````````````````````

Subscriptions will most often be created by the application, for an
entire group of entities. In this case, all the entities will receive
the notification, unless they later opt out. Subscriptions can also be
created for an individual entity to receive a certain type of
notification, as an opt-in subscription.

This library includes the table ``Subscription``, available from
``entity_subscription.models.Subscription``. Creating a
``Subscription`` object is straightforward, assuming the relevant
``Source`` and ``Medium`` objects have been created (See "Sources and
Mediums" above), and the entities to be subscribed and their group are
appropriately mirrored. From there, we can use the standard
``objects.create`` interface.

Given the sources and mediums created above, and a relationship
between ``MyUser`` and ``MyGroup`` in a given application, the
following is a subscription for all the users in a particular group:

.. code:: Python

    from my_app.models import MyUser
    from my_app.models import MyGroup

    from entity.models import Entity, EntityKind
    from entity_subscription.models import Subscription, Source, Medium

    super_entity = MyGroup.objects.get(name='product_group')
    Subscription.objects.create(
        medium = Medium.objects.get(name='in_site'),
        source = Source.objects.get(name='new_products'),
        entity = Entity.objects.get_for_obj(super_entity),
        subentity_kind = EntityKind.objects.get(name='myuser')
    )

Each ``Subscription`` object stored in the database only subscribes
the group of entities to a single combination of a ``Source`` and
``Medium``. To create subscriptions for delivering notifications from
the same source over different mediums, a new ``Subscription`` object
must be created for each source/medium combination.  This allows the
application developer and the users to have detailed control over what
the users are notified about, and how those notifications are
delivered.


Unsubscribing
``````````````````````````````````````````````````

Individual users of your application may wish to remove themselves
from receiving certain types of notifications.

To unsubscribe an individual from from receiving notifications of a
given source/medium combination is as simple as creating an
``Unsubscribe`` object. Assuming that "Robert" was subscribed to New
Product notifications in the subscription object above, unsubscribing
him from these notifications looks like:

.. code:: Python

    from my_app.models import MyUser

    from entity.models import Entity
    from entity_subscription.models import Unsubscribe, Source, Medium

    Robert = MyUser.objects.get(name='Robert')

    Unsubscribe.objects.create(
        entity = Entity.objects.get_for_obj(Robert)
        medium = Medium.objects.get(name='in_site')
        sorce = Source.objects.get(name='new_products')
    )

With this object created, the rest of the group will receive these
notifications still, however "Robert" will no longer see them.

Subscriptions and Unsubscribing Considerations
``````````````````````````````````````````````````

Separating subscriptions and unsubscriptions into separate tables
allows for groups of entities to be subscribed with a single object in
the ``Subscription`` table. This is useful for subscribing large
groups of users to a notification by default.

If a given notification may only have a few users interested in
receiving, it may make more sense for it to be an opt-in notification,
where a Subscription object is made for each single entity that wishes
to opt in (that is, a ``Subscription`` object with a
``subentity_kind=None``). This may make more sense then subscribing
large groups to this notification and having most of them unsubscribe.


Checking Subscriptions
--------------------------------------------------

Once your sites subscriptions are stored as shown above, you will want
to use those subscriptions to decide to deliver (or not deliver)
notifications. The ``entity_subscription`` app provides a couple
methods to make it easier to find who is subscribed to what.

The ``SubscriptionManager``
  The following methods are available from the manager of the
  ``Subscription`` model.

  ``mediums_subscribed(source, entity, subentity_kind=None)``
    Return a queryset of all the mediums the given ``entity`` is
    subscribed to, for the given ``source``.

    If the optional ``subentity_kind`` parameter is given, return
    *every* medium that any of the given ``entity``'s sub-entities, of
    the given ``EntityKind``, is subscribed to.

  ``is_subscribed(source, medium, entity, subentity_kind=None)``
    Return a Boolean, indicating if the entity is subscribed to the
    given ``source`` on the given ``medium``.

    If the optional ``subentity_kind`` parameter is not ``None``,
    return ``True`` if *any* of the ``entity``'s sub-entities, of the
    given type, are subscribed to the given ``source`` on the given
    ``medium``.

In the common case, checking for subscriptions involves looking at the
mediums a single entity is subscribed to. In this case both
``mediums_subscribed`` and ``is_subscribed`` should behave exactly as
expected. Their exact behavior is described in more detail below, in
the section "Checking if an individual entity is subscribed".

The implications of including a ``subentity_kind`` argument are
somewhat more subtle. These implications are described in more detail
below, in the section "Checking if anyone in a group is subscribed".


Checking if an individual entity is subscribed
``````````````````````````````````````````````````

Before sending notifications to users, your application wants to make
sure that it's sending those notifications to users who have been
included through a subscription, and not excluded themselves by
unsubscribing.

To check the subscription status of a single entity, simply call
``mediums_subscribed`` if you want a list of all the mediums an entity
is subscribed to, for a given source, or call ``is_subscribed`` if you
want to check if that entity is subscribed to a particular medium for
a given source. When checking the subscription status of a single
entity, the ``subentity_kind`` argument should be left as ``None``.

When ``mediums_subscribed`` or ``is_subscribed`` are called without a
``subentity_kind`` argument, the behavior of these methods is
straightforward. They will return a medium, or return true for that
medium, only if:

1. The entity is part of a individual subscription, or is part of a
group subscription for the given source.

2. The entity is not unsubscribed from that source and medium.

Once you have checked that an individual entity is subscribed to a
given source/medium combination, you can be confident in delivering
that notification.


Checking if anyone in a group is subscribed
``````````````````````````````````````````````````

In some cases, your application may have an event that applies to a
group of individuals, and you may wish to check if any of those
individuals are subscribed to receive notifications for that
event.

Both ``mediums_subscribed`` and ``is_subscribed`` can also take an
optional parameter ``subentity_kind`` which will change their
behavior fairly significantly. In this case, the provided argument,
``entity``, is assumed to be a super-entity, and these functions
return values based on what *any* of the sub entities are subscribed
to.

So, passing in a super-entity, and subentity-type to either
``mediums_subscribed`` or ``is_subscribed`` can provide a useful start
for delivering notifications.

Note that this is only an *approximation* of what individuals in the
group are subscribed to. Before actually delivering a notification
to any subentity, the application must check that each user is
actually subscribed to receive that notification.


Filtering entities based on subscriptions
``````````````````````````````````````````````````

Given some number of entities, that may or may not be subscribed to
notifications from a given source and medium, it could be complicated
to determine all the possible entity relationships, and the relevant
subscriptions and unsubscriptions to check exactly which of those
entities should be notified. The entity-subscription framework
provides a method, ``Subscription.objects.filter_not_subscribed`` that
will take the list of entities and return only those that should
definitely recieve the notification.

.. code:: Python

   entities = [entity_1, entity_2, entity_3]
   subscribed_entities = Subscription.objects.filter_not_subscribed(source, medium, entities)

This method returns a queryset of entities to be notified. It takes
into account all possible group subscriptions the entities may belong
to, as well as removing entities that are unsubscribed from these
notifications.

It does, require, however, that all the entities provided are of the
same ``entity_kind``.


Release notes
``````````````````````````````````````````````````

* 0.4.0

    * Migrated Django Entity Subscription to use the ``EntityKind`` model for specifying
        different kinds of entities. This was a new addition in Django Entity 1.5. Schema migrations
        are provided that remove the ``subentity_type`` ``ContentType`` variable from the ``Subscription``
        model and add the ``subentity_kind`` ``EntityKind`` variable.
