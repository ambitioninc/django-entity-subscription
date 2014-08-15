# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'entity_subscription_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('render_class_path', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'entity_subscription', ['Action'])

        # Deleting field 'Notification.subentity_type'
        db.delete_column(u'entity_subscription_notification', 'subentity_type_id')

        # Deleting field 'Notification.source'
        db.delete_column(u'entity_subscription_notification', 'source_id')

        # Deleting field 'Notification.uuid'
        db.delete_column(u'entity_subscription_notification', 'uuid')

        # Deleting field 'Notification.time_sent'
        db.delete_column(u'entity_subscription_notification', 'time_sent')

        # Deleting field 'Notification.entity'
        db.delete_column(u'entity_subscription_notification', 'entity_id')

        # Adding field 'Notification.actor'
        db.add_column(u'entity_subscription_notification', 'actor',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity.Entity']),
                      keep_default=False)

        # Adding field 'Notification.action'
        db.add_column(u'entity_subscription_notification', 'action',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_subscription.Action']),
                      keep_default=False)

        # Adding field 'Notification.action_object'
        db.add_column(u'entity_subscription_notification', 'action_object',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='+', null=True, to=orm['entity.Entity']),
                      keep_default=False)

        # Adding field 'Notification.target'
        db.add_column(u'entity_subscription_notification', 'target',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='+', null=True, to=orm['entity.Entity']),
                      keep_default=False)

        # Adding field 'Notification.time_created'
        db.add_column(u'entity_subscription_notification', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=None, blank=True),
                      keep_default=False)

        # Adding field 'Notification.event_id'
        db.add_column(u'entity_subscription_notification', 'event_id',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Action'
        db.delete_table(u'entity_subscription_action')

        # Adding field 'Notification.subentity_type'
        db.add_column(u'entity_subscription_notification', 'subentity_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Notification.source'
        raise RuntimeError("Cannot reverse this migration. 'Notification.source' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Notification.source'
        db.add_column(u'entity_subscription_notification', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_subscription.Source']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Notification.uuid'
        raise RuntimeError("Cannot reverse this migration. 'Notification.uuid' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Notification.uuid'
        db.add_column(u'entity_subscription_notification', 'uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=128, unique=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Notification.time_sent'
        raise RuntimeError("Cannot reverse this migration. 'Notification.time_sent' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Notification.time_sent'
        db.add_column(u'entity_subscription_notification', 'time_sent',
                      self.gf('django.db.models.fields.DateTimeField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Notification.entity'
        raise RuntimeError("Cannot reverse this migration. 'Notification.entity' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Notification.entity'
        db.add_column(u'entity_subscription_notification', 'entity',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity.Entity']),
                      keep_default=False)

        # Deleting field 'Notification.actor'
        db.delete_column(u'entity_subscription_notification', 'actor_id')

        # Deleting field 'Notification.action'
        db.delete_column(u'entity_subscription_notification', 'action_id')

        # Deleting field 'Notification.action_object'
        db.delete_column(u'entity_subscription_notification', 'action_object_id')

        # Deleting field 'Notification.target'
        db.delete_column(u'entity_subscription_notification', 'target_id')

        # Deleting field 'Notification.time_created'
        db.delete_column(u'entity_subscription_notification', 'time_created')

        # Deleting field 'Notification.event_id'
        db.delete_column(u'entity_subscription_notification', 'event_id')


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
            'render_class_path': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'entity_subscription.medium': {
            'Meta': {'object_name': 'Medium'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'entity_subscription.notification': {
            'Meta': {'object_name': 'Notification'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Action']"}),
            'action_object': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': u"orm['entity.Entity']"}),
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            'context': ('jsonfield.fields.JSONField', [], {}),
            'event_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'+'", 'null': 'True', 'to': u"orm['entity.Entity']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        u'entity_subscription.notificationmedium': {
            'Meta': {'object_name': 'NotificationMedium'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Notification']"}),
            'time_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        u'entity_subscription.source': {
            'Meta': {'object_name': 'Source'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'entity_subscription.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Source']"}),
            'subentity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'})
        },
        u'entity_subscription.unsubscribe': {
            'Meta': {'object_name': 'Unsubscribe'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Source']"})
        }
    }

    complete_apps = ['entity_subscription']