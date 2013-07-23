# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteContent'
        db.create_table('reanalyseapp_sitecontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('contenthtml', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('reanalyseapp', ['SiteContent'])

        # Adding model 'Tag'
        db.create_table('reanalyseapp_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('reanalyseapp', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['type', 'slug']
        db.create_unique('reanalyseapp_tag', ['type', 'slug'])

        # Adding model 'Enquete'
        db.create_table('reanalyseapp_enquete', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('uploadpath', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('locationpath', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('metadata', self.gf('django.db.models.fields.TextField')(default='{}')),
            ('ese', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('statuscomplete', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ddi_id', self.gf('django.db.models.fields.CharField')(max_length=170)),
        ))
        db.send_create_signal('reanalyseapp', ['Enquete'])

        # Adding M2M table for field tags on 'Enquete'
        m2m_table_name = db.shorten_name('reanalyseapp_enquete_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enquete', models.ForeignKey(orm['reanalyseapp.enquete'], null=False)),
            ('tag', models.ForeignKey(orm['reanalyseapp.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['enquete_id', 'tag_id'])

        # Adding model 'AccessRequest'
        db.create_table('reanalyseapp_accessrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(related_name='access_requests', to=orm['reanalyseapp.Enquete'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_activated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('reanalyseapp', ['AccessRequest'])

        # Adding unique constraint on 'AccessRequest', fields ['user', 'enquete']
        db.create_unique('reanalyseapp_accessrequest', ['user_id', 'enquete_id'])

        # Adding model 'Visualization'
        db.create_table('reanalyseapp_visualization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('locationpath', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('viztype', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('contenthtml', self.gf('django.db.models.fields.TextField')()),
            ('json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('reanalyseapp', ['Visualization'])

        # Adding M2M table for field textes on 'Visualization'
        m2m_table_name = db.shorten_name('reanalyseapp_visualization_textes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visualization', models.ForeignKey(orm['reanalyseapp.visualization'], null=False)),
            ('texte', models.ForeignKey(orm['reanalyseapp.texte'], null=False))
        ))
        db.create_unique(m2m_table_name, ['visualization_id', 'texte_id'])

        # Adding M2M table for field speakers on 'Visualization'
        m2m_table_name = db.shorten_name('reanalyseapp_visualization_speakers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visualization', models.ForeignKey(orm['reanalyseapp.visualization'], null=False)),
            ('speaker', models.ForeignKey(orm['reanalyseapp.speaker'], null=False))
        ))
        db.create_unique(m2m_table_name, ['visualization_id', 'speaker_id'])

        # Adding model 'Texte'
        db.create_table('reanalyseapp_texte', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('locationpath', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('filesize', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('doctype', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('doccat1', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('doccat2', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 7, 23, 0, 0))),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('locationgeo', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('statuscomplete', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('contenttxt', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('contenthtml', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('contentxml', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('reanalyseapp', ['Texte'])

        # Adding M2M table for field tags on 'Texte'
        m2m_table_name = db.shorten_name('reanalyseapp_texte_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('texte', models.ForeignKey(orm['reanalyseapp.texte'], null=False)),
            ('tag', models.ForeignKey(orm['reanalyseapp.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['texte_id', 'tag_id'])

        # Adding model 'AttributeType'
        db.create_table('reanalyseapp_attributetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('publicy', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('reanalyseapp', ['AttributeType'])

        # Adding model 'Attribute'
        db.create_table('reanalyseapp_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('attributetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.AttributeType'])),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('reanalyseapp', ['Attribute'])

        # Adding model 'Speaker'
        db.create_table('reanalyseapp_speaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('ddi_id', self.gf('django.db.models.fields.CharField')(max_length=170)),
            ('ddi_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('color', self.gf('django.db.models.fields.CharField')(default='#FADFCA', max_length=7)),
            ('contenttxt', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('reanalyseapp', ['Speaker'])

        # Adding M2M table for field textes on 'Speaker'
        m2m_table_name = db.shorten_name('reanalyseapp_speaker_textes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('speaker', models.ForeignKey(orm['reanalyseapp.speaker'], null=False)),
            ('texte', models.ForeignKey(orm['reanalyseapp.texte'], null=False))
        ))
        db.create_unique(m2m_table_name, ['speaker_id', 'texte_id'])

        # Adding M2M table for field attributes on 'Speaker'
        m2m_table_name = db.shorten_name('reanalyseapp_speaker_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('speaker', models.ForeignKey(orm['reanalyseapp.speaker'], null=False)),
            ('attribute', models.ForeignKey(orm['reanalyseapp.attribute'], null=False))
        ))
        db.create_unique(m2m_table_name, ['speaker_id', 'attribute_id'])

        # Adding model 'SpeakerSet'
        db.create_table('reanalyseapp_speakerset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('reanalyseapp', ['SpeakerSet'])

        # Adding M2M table for field speakers on 'SpeakerSet'
        m2m_table_name = db.shorten_name('reanalyseapp_speakerset_speakers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('speakerset', models.ForeignKey(orm['reanalyseapp.speakerset'], null=False)),
            ('speaker', models.ForeignKey(orm['reanalyseapp.speaker'], null=False))
        ))
        db.create_unique(m2m_table_name, ['speakerset_id', 'speaker_id'])

        # Adding model 'Code'
        db.create_table('reanalyseapp_code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('reanalyseapp', ['Code'])

        # Adding M2M table for field textes on 'Code'
        m2m_table_name = db.shorten_name('reanalyseapp_code_textes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('code', models.ForeignKey(orm['reanalyseapp.code'], null=False)),
            ('texte', models.ForeignKey(orm['reanalyseapp.texte'], null=False))
        ))
        db.create_unique(m2m_table_name, ['code_id', 'texte_id'])

        # Adding model 'Sentence'
        db.create_table('reanalyseapp_sentence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('texte', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Texte'])),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Speaker'])),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Code'])),
            ('contenttxt', self.gf('django.db.models.fields.TextField')()),
            ('contenthtml', self.gf('django.db.models.fields.TextField')()),
            ('i', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('o', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('n', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('reanalyseapp', ['Sentence'])

        # Adding model 'WordEntity'
        db.create_table('reanalyseapp_wordentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Code'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=400)),
            ('df', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('maxtfidf', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('maxspeakerid', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('reanalyseapp', ['WordEntity'])

        # Adding M2M table for field textes on 'WordEntity'
        m2m_table_name = db.shorten_name('reanalyseapp_wordentity_textes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordentity', models.ForeignKey(orm['reanalyseapp.wordentity'], null=False)),
            ('texte', models.ForeignKey(orm['reanalyseapp.texte'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordentity_id', 'texte_id'])

        # Adding model 'WordEntitySpeaker'
        db.create_table('reanalyseapp_wordentityspeaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Speaker'])),
            ('wordentity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.WordEntity'])),
            ('tf', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('tfidf', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('reanalyseapp', ['WordEntitySpeaker'])

        # Adding M2M table for field textes on 'WordEntitySpeaker'
        m2m_table_name = db.shorten_name('reanalyseapp_wordentityspeaker_textes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordentityspeaker', models.ForeignKey(orm['reanalyseapp.wordentityspeaker'], null=False)),
            ('texte', models.ForeignKey(orm['reanalyseapp.texte'], null=False))
        ))
        db.create_unique(m2m_table_name, ['wordentityspeaker_id', 'texte_id'])

        # Adding model 'Word'
        db.create_table('reanalyseapp_word', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('wordentityspeaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.WordEntitySpeaker'])),
            ('sentence', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Sentence'])),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Speaker'])),
            ('n', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
        ))
        db.send_create_signal('reanalyseapp', ['Word'])

        # Adding model 'Ngram'
        db.create_table('reanalyseapp_ngram', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('df', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('reanalyseapp', ['Ngram'])

        # Adding model 'NgramSpeaker'
        db.create_table('reanalyseapp_ngramspeaker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enquete', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Enquete'])),
            ('ngram', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Ngram'])),
            ('speaker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reanalyseapp.Speaker'])),
            ('tf', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('tn', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('tfidf', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('reanalyseapp', ['NgramSpeaker'])


    def backwards(self, orm):
        # Removing unique constraint on 'AccessRequest', fields ['user', 'enquete']
        db.delete_unique('reanalyseapp_accessrequest', ['user_id', 'enquete_id'])

        # Removing unique constraint on 'Tag', fields ['type', 'slug']
        db.delete_unique('reanalyseapp_tag', ['type', 'slug'])

        # Deleting model 'SiteContent'
        db.delete_table('reanalyseapp_sitecontent')

        # Deleting model 'Tag'
        db.delete_table('reanalyseapp_tag')

        # Deleting model 'Enquete'
        db.delete_table('reanalyseapp_enquete')

        # Removing M2M table for field tags on 'Enquete'
        db.delete_table(db.shorten_name('reanalyseapp_enquete_tags'))

        # Deleting model 'AccessRequest'
        db.delete_table('reanalyseapp_accessrequest')

        # Deleting model 'Visualization'
        db.delete_table('reanalyseapp_visualization')

        # Removing M2M table for field textes on 'Visualization'
        db.delete_table(db.shorten_name('reanalyseapp_visualization_textes'))

        # Removing M2M table for field speakers on 'Visualization'
        db.delete_table(db.shorten_name('reanalyseapp_visualization_speakers'))

        # Deleting model 'Texte'
        db.delete_table('reanalyseapp_texte')

        # Removing M2M table for field tags on 'Texte'
        db.delete_table(db.shorten_name('reanalyseapp_texte_tags'))

        # Deleting model 'AttributeType'
        db.delete_table('reanalyseapp_attributetype')

        # Deleting model 'Attribute'
        db.delete_table('reanalyseapp_attribute')

        # Deleting model 'Speaker'
        db.delete_table('reanalyseapp_speaker')

        # Removing M2M table for field textes on 'Speaker'
        db.delete_table(db.shorten_name('reanalyseapp_speaker_textes'))

        # Removing M2M table for field attributes on 'Speaker'
        db.delete_table(db.shorten_name('reanalyseapp_speaker_attributes'))

        # Deleting model 'SpeakerSet'
        db.delete_table('reanalyseapp_speakerset')

        # Removing M2M table for field speakers on 'SpeakerSet'
        db.delete_table(db.shorten_name('reanalyseapp_speakerset_speakers'))

        # Deleting model 'Code'
        db.delete_table('reanalyseapp_code')

        # Removing M2M table for field textes on 'Code'
        db.delete_table(db.shorten_name('reanalyseapp_code_textes'))

        # Deleting model 'Sentence'
        db.delete_table('reanalyseapp_sentence')

        # Deleting model 'WordEntity'
        db.delete_table('reanalyseapp_wordentity')

        # Removing M2M table for field textes on 'WordEntity'
        db.delete_table(db.shorten_name('reanalyseapp_wordentity_textes'))

        # Deleting model 'WordEntitySpeaker'
        db.delete_table('reanalyseapp_wordentityspeaker')

        # Removing M2M table for field textes on 'WordEntitySpeaker'
        db.delete_table(db.shorten_name('reanalyseapp_wordentityspeaker_textes'))

        # Deleting model 'Word'
        db.delete_table('reanalyseapp_word')

        # Deleting model 'Ngram'
        db.delete_table('reanalyseapp_ngram')

        # Deleting model 'NgramSpeaker'
        db.delete_table('reanalyseapp_ngramspeaker')


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
        'reanalyseapp.accessrequest': {
            'Meta': {'unique_together': "(('user', 'enquete'),)", 'object_name': 'AccessRequest'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'access_requests'", 'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'reanalyseapp.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'attributetype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.AttributeType']"}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'reanalyseapp.attributetype': {
            'Meta': {'object_name': 'AttributeType'},
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'publicy': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'reanalyseapp.code': {
            'Meta': {'object_name': 'Code'},
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'textes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Texte']", 'symmetrical': 'False'})
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
        'reanalyseapp.ngram': {
            'Meta': {'object_name': 'Ngram'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'df': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'reanalyseapp.ngramspeaker': {
            'Meta': {'object_name': 'NgramSpeaker'},
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ngram': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Ngram']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Speaker']"}),
            'tf': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tfidf': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tn': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'reanalyseapp.sentence': {
            'Meta': {'object_name': 'Sentence'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Code']"}),
            'contenthtml': ('django.db.models.fields.TextField', [], {}),
            'contenttxt': ('django.db.models.fields.TextField', [], {}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'i': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'o': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Speaker']"}),
            'texte': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Texte']"})
        },
        'reanalyseapp.sitecontent': {
            'Meta': {'object_name': 'SiteContent'},
            'contenthtml': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reanalyseapp.speaker': {
            'Meta': {'object_name': 'Speaker'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Attribute']", 'symmetrical': 'False'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#FADFCA'", 'max_length': '7'}),
            'contenttxt': ('django.db.models.fields.TextField', [], {}),
            'ddi_id': ('django.db.models.fields.CharField', [], {'max_length': '170'}),
            'ddi_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'textes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Texte']", 'symmetrical': 'False'})
        },
        'reanalyseapp.speakerset': {
            'Meta': {'object_name': 'SpeakerSet'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Speaker']", 'symmetrical': 'False'})
        },
        'reanalyseapp.tag': {
            'Meta': {'ordering': "['type', 'slug']", 'unique_together': "(('type', 'slug'),)", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'reanalyseapp.texte': {
            'Meta': {'object_name': 'Texte'},
            'contenthtml': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contenttxt': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'contentxml': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 7, 23, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'doccat1': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'doccat2': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'doctype': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'filesize': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'locationgeo': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'locationpath': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'statuscomplete': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Tag']", 'symmetrical': 'False'})
        },
        'reanalyseapp.visualization': {
            'Meta': {'object_name': 'Visualization'},
            'contenthtml': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'locationpath': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Speaker']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'textes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Texte']", 'symmetrical': 'False'}),
            'viztype': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'reanalyseapp.word': {
            'Meta': {'object_name': 'Word'},
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'sentence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Sentence']"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Speaker']"}),
            'wordentityspeaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.WordEntitySpeaker']"})
        },
        'reanalyseapp.wordentity': {
            'Meta': {'object_name': 'WordEntity'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Code']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '400'}),
            'df': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'enquete': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Enquete']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxspeakerid': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'maxtfidf': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'textes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Texte']", 'symmetrical': 'False'})
        },
        'reanalyseapp.wordentityspeaker': {
            'Meta': {'object_name': 'WordEntitySpeaker'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.Speaker']"}),
            'textes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reanalyseapp.Texte']", 'symmetrical': 'False'}),
            'tf': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tfidf': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'wordentity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reanalyseapp.WordEntity']"})
        }
    }

    complete_apps = ['reanalyseapp']