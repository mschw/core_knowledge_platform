# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Keyword'
        db.create_table('core_web_service_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('core_web_service', ['Keyword'])

        # Adding model 'PaperGroup'
        db.create_table('core_web_service_papergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('blind_review', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core_web_service', ['PaperGroup'])

        # Adding M2M table for field editors on 'PaperGroup'
        db.create_table('core_web_service_papergroup_editors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('papergroup', models.ForeignKey(orm['core_web_service.papergroup'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('core_web_service_papergroup_editors', ['papergroup_id', 'user_id'])

        # Adding M2M table for field referees on 'PaperGroup'
        db.create_table('core_web_service_papergroup_referees', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('papergroup', models.ForeignKey(orm['core_web_service.papergroup'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('core_web_service_papergroup_referees', ['papergroup_id', 'user_id'])

        # Adding M2M table for field publications on 'PaperGroup'
        db.create_table('core_web_service_papergroup_publications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('papergroup', models.ForeignKey(orm['core_web_service.papergroup'], null=False)),
            ('publication', models.ForeignKey(orm['core_web_service.publication'], null=False))
        ))
        db.create_unique('core_web_service_papergroup_publications', ['papergroup_id', 'publication_id'])

        # Adding M2M table for field tags on 'PaperGroup'
        db.create_table('core_web_service_papergroup_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('papergroup', models.ForeignKey(orm['core_web_service.papergroup'], null=False)),
            ('tag', models.ForeignKey(orm['core_web_service.tag'], null=False))
        ))
        db.create_unique('core_web_service_papergroup_tags', ['papergroup_id', 'tag_id'])

        # Adding field 'Publication.abstract'
        db.add_column('core_web_service_publication', 'abstract', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Publication.review_status'
        db.add_column('core_web_service_publication', 'review_status', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding M2M table for field keywords on 'Publication'
        db.create_table('core_web_service_publication_keywords', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publication', models.ForeignKey(orm['core_web_service.publication'], null=False)),
            ('keyword', models.ForeignKey(orm['core_web_service.keyword'], null=False))
        ))
        db.create_unique('core_web_service_publication_keywords', ['publication_id', 'keyword_id'])


    def backwards(self, orm):
        
        # Deleting model 'Keyword'
        db.delete_table('core_web_service_keyword')

        # Deleting model 'PaperGroup'
        db.delete_table('core_web_service_papergroup')

        # Removing M2M table for field editors on 'PaperGroup'
        db.delete_table('core_web_service_papergroup_editors')

        # Removing M2M table for field referees on 'PaperGroup'
        db.delete_table('core_web_service_papergroup_referees')

        # Removing M2M table for field publications on 'PaperGroup'
        db.delete_table('core_web_service_papergroup_publications')

        # Removing M2M table for field tags on 'PaperGroup'
        db.delete_table('core_web_service_papergroup_tags')

        # Deleting field 'Publication.abstract'
        db.delete_column('core_web_service_publication', 'abstract')

        # Deleting field 'Publication.review_status'
        db.delete_column('core_web_service_publication', 'review_status')

        # Removing M2M table for field keywords on 'Publication'
        db.delete_table('core_web_service_publication_keywords')


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
        'core_web_service.author': {
            'Meta': {'object_name': 'Author'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core_web_service.comment': {
            'Meta': {'object_name': 'Comment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Vote']"})
        },
        'core_web_service.esteem': {
            'Meta': {'object_name': 'Esteem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'core_web_service.furtherfields': {
            'Meta': {'object_name': 'FurtherFields'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Publication']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'core_web_service.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'core_web_service.papergroup': {
            'Meta': {'object_name': 'PaperGroup'},
            'blind_review': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'papergroup_editors'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publications': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.Publication']", 'symmetrical': 'False'}),
            'referees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'papergroup_referees'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core_web_service.peerreview': {
            'Meta': {'object_name': 'PeerReview'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peer_reviewer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Publication']"}),
            'review': ('django.db.models.fields.TextField', [], {}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.PeerReviewTemplate']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core_web_service.peerreviewtemplate': {
            'Meta': {'object_name': 'PeerReviewTemplate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template_binary_path': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'template_text': ('django.db.models.fields.TextField', [], {})
        },
        'core_web_service.publication': {
            'Meta': {'object_name': 'Publication'},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.Author']", 'symmetrical': 'False'}),
            'booktitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.Comment']", 'symmetrical': 'False'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'how_published': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.Keyword']", 'symmetrical': 'False'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publication_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'review_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'core_web_service.rating': {
            'Meta': {'object_name': 'Rating'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Publication']"}),
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'})
        },
        'core_web_service.referencematerial': {
            'Meta': {'object_name': 'ReferenceMaterial'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Publication']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core_web_service.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '511'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '75', 'db_index': 'True'})
        },
        'core_web_service.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'authenticated_professional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'further_fields': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.FurtherFields']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'core_web_service.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['core_web_service']
