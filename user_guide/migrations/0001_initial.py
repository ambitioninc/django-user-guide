# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Guide'
        db.create_table(u'user_guide_guide', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html', self.gf('django.db.models.fields.TextField')(max_length=256)),
            ('guide_type', self.gf('django.db.models.fields.CharField')(default='WINDOW', max_length=16)),
            ('guide_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('guide_tag', self.gf('django.db.models.fields.CharField')(default='all', max_length=256)),
            ('guide_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'user_guide', ['Guide'])

        # Adding model 'GuideInfo'
        db.create_table(u'user_guide_guideinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('guide', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['user_guide.Guide'])),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('finished_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'user_guide', ['GuideInfo'])

        # Adding unique constraint on 'GuideInfo', fields ['user', 'guide']
        db.create_unique(u'user_guide_guideinfo', ['user_id', 'guide_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'GuideInfo', fields ['user', 'guide']
        db.delete_unique(u'user_guide_guideinfo', ['user_id', 'guide_id'])

        # Deleting model 'Guide'
        db.delete_table(u'user_guide_guide')

        # Deleting model 'GuideInfo'
        db.delete_table(u'user_guide_guideinfo')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'user_guide.guide': {
            'Meta': {'object_name': 'Guide'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guide_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'guide_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'guide_tag': ('django.db.models.fields.CharField', [], {'default': "'all'", 'max_length': '256'}),
            'guide_type': ('django.db.models.fields.CharField', [], {'default': "'WINDOW'", 'max_length': '16'}),
            'html': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'user_guide.guideinfo': {
            'Meta': {'unique_together': "(('user', 'guide'),)", 'object_name': 'GuideInfo'},
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'finished_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'guide': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_guide.Guide']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['user_guide']