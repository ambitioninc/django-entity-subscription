# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Source'
        db.delete_table(u'entity_subscription_source')

        # Deleting field 'Subscription.source'
        db.delete_column(u'entity_subscription_subscription', 'source_id')

        # Adding field 'Subscription.action'
        db.add_column(u'entity_subscription_subscription', 'action',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_subscription.Action']),
                      keep_default=False)

        # Deleting field 'Unsubscribe.source'
        db.delete_column(u'entity_subscription_unsubscribe', 'source_id')

        # Adding field 'Unsubscribe.action'
        db.add_column(u'entity_subscription_unsubscribe', 'action',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_subscription.Action']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Source'
        db.create_table(u'entity_subscription_source', (
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'entity_subscription', ['Source'])


        # User chose to not deal with backwards NULL issues for 'Subscription.source'
        raise RuntimeError("Cannot reverse this migration. 'Subscription.source' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Subscription.source'
        db.add_column(u'entity_subscription_subscription', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entity_subscription.Source']),
                      keep_default=False)

        # Deleting field 'Subscription.action'
        db.delete_column(u'entity_subscription_subscription', 'action_id')

        # Adding field 'Unsubscribe.source'
        db.add_column(u'entity_subscription_unsubscribe', 'source',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['entity_subscription.Source']),
                      keep_default=False)

        # Deleting field 'Unsubscribe.action'
        db.delete_column(u'entity_subscription_unsubscribe', 'action_id')


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
        u'entity_subscription.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Action']"}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"}),
            'subentity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'})
        },
        u'entity_subscription.unsubscribe': {
            'Meta': {'object_name': 'Unsubscribe'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Action']"}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['entity_subscription.Medium']"})
        }
    }

    complete_apps = ['entity_subscription']