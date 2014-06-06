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

all avaliable from within the package ``entity_subscription.models``.

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

For any given source, users may want to recieve notifications over
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
        description='Tells you whenver a new item is available in the store.'
    )


Mediums
``````````````````````````````````````````````````

From a user of your application's perspective a "medium" is a way in
which they can be notified. Your site may support a variety of
differenty mediums for notifying your users of different
happenings. Examples could include Email, Text Messages, a News-Feed,
or a In-site Notification center.

Users will likely want to recieve notifications through some
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


Considerations
``````````````````````````````````````````````````

Both ``Source`` and ``Medium`` objects can be effectively used as
static records that are setup as initial data for an application, or
as dynamic records that change as the various sources and mediums for
notification change. It is important to consider, however, that
excessively dynamic sources and mediums will make it difficult for
indifidual entities to control their subscriptions.
