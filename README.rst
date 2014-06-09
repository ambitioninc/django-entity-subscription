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

    from django.contrib.contenttypes.models import ContentType
    from entity.models import Entity
    from entity_subscription.models import Subscription, Source, Medium

    super_entity = MyGroup.objects.get(name='product_group')
    Subscription.objects.create(
        medium = Medium.objects.get(name='in_site'),
        source = Source.objects.get(name='new_products'),
        entity = Entity.objects.get_for_obj(super_entity),
        subentity_type = ContentType.get_for_model(MyUser)
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
``subentity_type=None``). This may make more sense then subscribing
large groups to this notification and having most of them unsubscribe.
