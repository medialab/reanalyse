# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('outside_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('outside', ['Message'])

        # Adding model 'Enquiry'
        db.create_table('outside_enquiry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=160, null=True, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='EN', max_length=2)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('activated', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enquiry', to=orm['reanalyseapp.Enquete'])),
        ))
        db.send_create_signal('outside', ['Enquiry'])

        # Adding unique constraint on 'Enquiry', fields ['enquete', 'language']
        db.create_unique('outside_enquiry', ['enquete_id', 'language'])

        # Adding M2M table for field pins on 'Enquiry'
        m2m_table_name = db.shorten_name('outside_enquiry_pins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enquiry', models.ForeignKey(orm['outside.enquiry'], null=False)),
            ('pin', models.ForeignKey(orm['glue.pin'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enquiry_id', 'pin_id'])

        # Adding M2M table for field tags on 'Enquiry'
        m2m_table_name = db.shorten_name('outside_enquiry_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enquiry', models.ForeignKey(orm['outside.enquiry'], null=False)),
            ('tag', models.ForeignKey(orm['reanalyseapp.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enquiry_id', 'tag_id'])

        # Adding model 'Subscriber'
        db.create_table('outside_subscriber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('email_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('affiliation', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('accepted_terms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('confirmation_code', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('outside', ['Subscriber'])

        # Adding M2M table for field messages on 'Subscriber'
        m2m_table_name = db.shorten_name('outside_subscriber_messages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscriber', models.ForeignKey(orm['outside.subscriber'], null=False)),
            ('message', models.ForeignKey(orm['outside.message'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscriber_id', 'message_id'])

        # Adding model 'Confirmation_code'
        db.create_table('outside_confirmation_code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('activated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('outside', ['Confirmation_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'Enquiry', fields ['enquete', 'language']
        db.delete_unique('outside_enquiry', ['enquete_id', 'language'])

        # Deleting model 'Message'
        db.delete_table('outside_message')

        # Deleting model 'Enquiry'
        db.delete_table('outside_enquiry')

        # Removing M2M table for field pins on 'Enquiry'
        db.delete_table(db.shorten_name('outside_enquiry_pins'))

        # Removing M2M table for field tags on 'Enquiry'
        db.delete_table(db.shorten_name('outside_enquiry_tags'))

        # Deleting model 'Subscriber'
        db.delete_table('outside_subscriber')

        # Removing M2M table for field messages on 'Subscriber'
        db.delete_table(db.shorten_name('outside_subscriber_messages'))

        # Deleting model 'Confirmation_code'
        db.delete_table('outside_confirmation_code')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'glue.geo': {
            'Meta': {'object_name': 'Geo'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'zoom': ('django.db.models.fields.IntegerField', [], {})
        },
        'glue.pin': {
            'Meta': {'ordering': "('sort', 'id')", 'unique_together': "(('slug', 'language'),)", 'object_name': 'Pin'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_last_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'geos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['glue.Geo']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'EN'", 'max_length': '2'}),
            'local': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['glue.Pin']"}),
            'permalink': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'related': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_rel_+'", 'null': 'True', 'to': "orm['glue.Pin']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'outside.confirmation_code': {
            'Meta': {'object_name': 'Confirmation_code'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'outside.enquiry': {
            'Meta': {'unique_together': "(('enquete', 'language'),)", 'object_name': 'Enquiry'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enquiry'", 'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'EN'", 'max_length': '2'}),
            'pins': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['glue.Pin']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reanalyseapp.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        'outside.message': {
            'Meta': {'object_name': 'Message'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'outside.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'accepted_terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'confirmation_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['outside.Message']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'reanalyseapp.accessrequest': {
            'Meta': {'unique_together': "(('user', 'enquete'),)", 'object_name': 'AccessRequest'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'access_requests'", 'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'reanalyseapp.enquete': {
            'Meta': {'object_name': 'Enquete'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ddi_id': ('django.db.models.fields.CharField', [], {'max_length': '170'}),
            'ese': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locationpath': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'metadata': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'statuscomplete': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Tag']", 'symmetrical': 'False'}),
            'uploadpath': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['reanalyseapp.AccessRequest']", 'symmetrical': 'False'})
        },
        'reanalyseapp.tag': {
            'Meta': {'ordering': "['type', 'slug']", 'unique_together': "(('type', 'slug'),)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['outside']