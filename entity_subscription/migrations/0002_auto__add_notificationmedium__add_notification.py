# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NotificationMedium'
        db.create_table(u'entity_subscription_notificationmedium', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_subscription.Notification'])),
            ('medium', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_subscription.Medium'])),
            ('time_seen', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
        ))
        db.send_create_signal(u'entity_subscription', ['NotificationMedium'])

        # Adding model 'Notification'
        db.create_table(u'entity_subscription_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity.Entity'])),
            ('subentity_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_subscription.Source'])),
            ('context', self.gf('jsonfield.fields.JSONField')()),
            ('time_sent', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_expires', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'entity_subscription', ['Notification'])


    def backwards(self, orm):
        # Deleting model 'NotificationMedium'
        db.delete_table(u'entity_subscription_notificationmedium')

        # Deleting model 'Notification'
        db.delete_table(u'entity_subscription_notification')


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
        u'entity_subscription.medium': {
            'Meta': {'object_name': 'Medium'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'entity_subscription.notification': {
            'Meta': {'object_name': 'Notification'},
            'context': ('jsonfield.fields.JSONField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Source']"}),
            'subentity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'time_expires': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'time_sent': ('django.db.models.fields.DateTimeField', [], {}),
            'uuid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
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