from django.core.urlresolvers import reverse


class BaseAction(object):

    def __init__(self, notification):
        self.notification = notification

    def render(self, html=True):
        render_str = '{0} {1} {2} {3}'.format(
            self.get_actor_display(self.notification.actor, html=html),
            self.get_action_display(self.notification.action, html=html),
            self.get_action_object_display(self.notification.action_object, html=html),
            self.get_target_display(self.notification.target, html=html),
        )
        return render_str.strip()

    def get_actor_display(self, actor, html=True):
        if html:
            return '<a href="{0}">{1}</a>'.format(self.get_actor_url(), self.get_actor_name(actor))
        return self.get_actor_name(actor)

    def get_action_display(self, action, html=True):
        return action.description

    def get_action_object_display(self, action_object, html=True):
        if not action_object:
            return ''
        if html:
            return '<a href="{0}">{1}</a>'.format(self.get_action_object_url(), action_object.entity)
        return action_object.entity

    def get_target_display(self, target, html=True):
        if not target:
            return ''
        if html:
            return 'to <a href="{0}">{1}</a>'.format(self.get_target_url(), target.entity)
        return 'to {0}'.format(target.entity)

    def get_actor_name(self, actor):
        if hasattr(actor, 'entity'):
            return actor.entity
        return actor

    def get_actor_url(self):
        if self.notification.context:
            if self.notification.context.get('actor_url'):
                return self.notification.context.get('actor_url')
            if self.notification.context.get('actor_url_name'):
                return reverse(self.notification.context.get('actor_url_name'), kwargs={
                    self.notification.context.get('actor_id_field', 'pk'): self.notification.context.get('actor_id'),
                })
        return None

    def get_action_object_name(self, action_object):
        if hasattr(action_object, 'entity'):
            return action_object.entity
        return action_object

    def get_action_object_url(self):
        if self.notification.context:
            if self.notification.context.get('action_object_url'):
                return self.notification.context.get('action_object_url')
            if self.notification.context.get('action_object_url_name'):
                return reverse(self.notification.context.get('action_object_url_name'), kwargs={
                    'pk': self.notification.context.get('action_object_id'),
                })
        return None

    def get_target_name(self, target):
        if hasattr(target, 'entity'):
            return target.entity
        return target

    def get_target_url(self):
        if self.notification.context:
            if self.notification.context.get('target_url'):
                return self.notification.context.get('target_url')
            if self.notification.context.get('target_url_name'):
                return reverse(self.notification.context.get('target_url_name'), kwargs={
                    'pk': self.notification.context.get('target_id'),
                })
        return None


class BaseMedium(object):

    def __init__(self, notification):
        self.notification = notification

    def render(self, notifications, html=True):
        rendered_notifications = [
            notification.render(html)
            for notification in notifications
        ]
        return rendered_notifications
