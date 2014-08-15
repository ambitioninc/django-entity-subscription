# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Notification', fields ['actor', 'event_id']
        db.delete_unique(u'entity_subscription_notification', ['actor_id', 'event_id'])

        # Deleting field 'Notification.target'
        db.delete_column(u'entity_subscription_notification', 'target_id')

        # Deleting field 'Notification.action_object'
        db.delete_column(u'entity_subscription_notification', 'action_object_id')

        # Deleting field 'Notification.actor'
        db.delete_column(u'entity_subscription_notification', 'actor_id')

        # Adding field 'Notification.actor_type'
        db.add_column(u'entity_subscription_notification', 'actor_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='+', to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'Notification.actor_id'
        db.add_column(u'entity_subscription_notification', 'actor_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=None),
                      keep_default=False)

        # Adding field 'Notification.action_object_type'
        db.add_column(u'entity_subscription_notification', 'action_object_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'Notification.action_object_id'
        db.add_column(u'entity_subscription_notification', 'action_object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Notification.target_type'
        db.add_column(u'entity_subscription_notification', 'target_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'Notification.target_id'
        db.add_column(u'entity_subscription_notification', 'target_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Notification.target'
        db.add_column(u'entity_subscription_notification', 'target',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='+', null=True, to=orm['entity.Entity']),
                      keep_default=False)

        # Adding field 'Notification.action_object'
        db.add_column(u'entity_subscription_notification', 'action_object',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='+', null=True, to=orm['entity.Entity']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Notification.actor'
        raise RuntimeError("Cannot reverse this migration. 'Notification.actor' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Notification.actor'
        db.add_column(u'entity_subscription_notification', 'actor',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity.Entity']),
                      keep_default=False)

        # Deleting field 'Notification.actor_type'
        db.delete_column(u'entity_subscription_notification', 'actor_type_id')

        # Deleting field 'Notification.actor_id'
        db.delete_column(u'entity_subscription_notification', 'actor_id')

        # Deleting field 'Notification.action_object_type'
        db.delete_column(u'entity_subscription_notification', 'action_object_type_id')

        # Deleting field 'Notification.action_object_id'
        db.delete_column(u'entity_subscription_notification', 'action_object_id')

        # Deleting field 'Notification.target_type'
        db.delete_column(u'entity_subscription_notification', 'target_type_id')

        # Deleting field 'Notification.target_id'
        db.delete_column(u'entity_subscription_notification', 'target_id')

        # Adding unique constraint on 'Notification', fields ['actor', 'event_id']
        db.create_unique(u'entity_subscription_notification', ['actor_id', 'event_id'])


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'entity.entity': {
            'Meta': {'object_name': 'Entity'},
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'entity_meta': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'entity_subscription.action': {
            'Meta': {'object_name': 'Action'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'render_class_path': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'})
        },
        u'entity_subscription.medium': {
            'Meta': {'object_name': 'Medium'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'render_class_path': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'})
        },
        u'entity_subscription.notification': {
            'Meta': {'object_name': 'Notification'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Action']"}),
            'action_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'action_object_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'actor_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'actor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['contenttypes.ContentType']"}),
            'context': ('jsonfield.fields.JSONField', [], {}),
            'event_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'target_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        u'entity_subscription.notificationmedium': {
            'Meta': {'object_name': 'NotificationMedium'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Notification']"}),
            'time_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        u'entity_subscription.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Action']", 'null': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            'followed_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['entity.Entity']"}),
            'followed_subentity_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"}),
            'subentity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'})
        },
        u'entity_subscription.unsubscribe': {
            'Meta': {'object_name': 'Unsubscribe'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Action']", 'null': 'True'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            'followed_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"})
        }
    }

    complete_apps = ['entity_subscription']