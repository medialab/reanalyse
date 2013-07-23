# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Geo'
        db.create_table('glue_geo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('zoom', self.gf('django.db.models.fields.IntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal('glue', ['Geo'])

        # Adding model 'Tag'
        db.create_table('glue_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('glue', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['type', 'slug']
        db.create_unique('glue_tag', ['type', 'slug'])

        # Adding model 'Pin'
        db.create_table('glue_pin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=160, null=True, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='EN', max_length=2)),
            ('mimetype', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_last_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('local', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('permalink', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['glue.Pin'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='D', max_length=2)),
        ))
        db.send_create_signal('glue', ['Pin'])

        # Adding unique constraint on 'Pin', fields ['slug', 'language']
        db.create_unique('glue_pin', ['slug', 'language'])

        # Adding M2M table for field related on 'Pin'
        m2m_table_name = db.shorten_name('glue_pin_related')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_pin', models.ForeignKey(orm['glue.pin'], null=False)),
            ('to_pin', models.ForeignKey(orm['glue.pin'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_pin_id', 'to_pin_id'])

        # Adding M2M table for field geos on 'Pin'
        m2m_table_name = db.shorten_name('glue_pin_geos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pin', models.ForeignKey(orm['glue.pin'], null=False)),
            ('geo', models.ForeignKey(orm['glue.geo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pin_id', 'geo_id'])

        # Adding M2M table for field users on 'Pin'
        m2m_table_name = db.shorten_name('glue_pin_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pin', models.ForeignKey(orm['glue.pin'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pin_id', 'user_id'])

        # Adding model 'Page'
        db.create_table('glue_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=160, null=True, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='EN', max_length=2)),
            ('sort', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('activated', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('glue', ['Page'])

        # Adding unique constraint on 'Page', fields ['slug', 'language']
        db.create_unique('glue_page', ['slug', 'language'])

        # Adding M2M table for field pins on 'Page'
        m2m_table_name = db.shorten_name('glue_page_pins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm['glue.page'], null=False)),
            ('pin', models.ForeignKey(orm['glue.pin'], null=False))
        ))
        db.create_unique(m2m_table_name, ['page_id', 'pin_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['slug', 'language']
        db.delete_unique('glue_page', ['slug', 'language'])

        # Removing unique constraint on 'Pin', fields ['slug', 'language']
        db.delete_unique('glue_pin', ['slug', 'language'])

        # Removing unique constraint on 'Tag', fields ['type', 'slug']
        db.delete_unique('glue_tag', ['type', 'slug'])

        # Deleting model 'Geo'
        db.delete_table('glue_geo')

        # Deleting model 'Tag'
        db.delete_table('glue_tag')

        # Deleting model 'Pin'
        db.delete_table('glue_pin')

        # Removing M2M table for field related on 'Pin'
        db.delete_table(db.shorten_name('glue_pin_related'))

        # Removing M2M table for field geos on 'Pin'
        db.delete_table(db.shorten_name('glue_pin_geos'))

        # Removing M2M table for field users on 'Pin'
        db.delete_table(db.shorten_name('glue_pin_users'))

        # Deleting model 'Page'
        db.delete_table('glue_page')

        # Removing M2M table for field pins on 'Page'
        db.delete_table(db.shorten_name('glue_page_pins'))


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
        'glue.page': {
            'Meta': {'unique_together': "(('slug', 'language'),)", 'object_name': 'Page'},
            'abstract': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'EN'", 'max_length': '2'}),
            'pins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'page'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['glue.Pin']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '160', 'null': 'True', 'blank': 'True'})
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
        'glue.tag': {
            'Meta': {'ordering': "['type', 'slug']", 'unique_together': "(('type', 'slug'),)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['glue']