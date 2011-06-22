# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Author'
        db.create_table('core_web_service_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('affiliation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
        ))
        db.send_create_signal('core_web_service', ['Author'])

        # Adding model 'Vote'
        db.create_table('core_web_service_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vote', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('core_web_service', ['Vote'])

        # Adding model 'Tag'
        db.create_table('core_web_service_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=511)),
        ))
        db.send_create_signal('core_web_service', ['Tag'])

        # Adding model 'Comment'
        db.create_table('core_web_service_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Vote'])),
        ))
        db.send_create_signal('core_web_service', ['Comment'])

        # Adding model 'Esteem'
        db.create_table('core_web_service_esteem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('User', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Tag'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core_web_service', ['Esteem'])

        # Adding model 'Publication'
        db.create_table('core_web_service_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('booktitle', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('chapter', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('editor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('how_published', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('publication_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('core_web_service', ['Publication'])

        # Adding M2M table for field authors on 'Publication'
        db.create_table('core_web_service_publication_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publication', models.ForeignKey(orm['core_web_service.publication'], null=False)),
            ('author', models.ForeignKey(orm['core_web_service.author'], null=False))
        ))
        db.create_unique('core_web_service_publication_authors', ['publication_id', 'author_id'])

        # Adding M2M table for field comments on 'Publication'
        db.create_table('core_web_service_publication_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publication', models.ForeignKey(orm['core_web_service.publication'], null=False)),
            ('comment', models.ForeignKey(orm['core_web_service.comment'], null=False))
        ))
        db.create_unique('core_web_service_publication_comments', ['publication_id', 'comment_id'])

        # Adding M2M table for field tags on 'Publication'
        db.create_table('core_web_service_publication_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publication', models.ForeignKey(orm['core_web_service.publication'], null=False)),
            ('tag', models.ForeignKey(orm['core_web_service.tag'], null=False))
        ))
        db.create_unique('core_web_service_publication_tags', ['publication_id', 'tag_id'])

        # Adding model 'FurtherFields'
        db.create_table('core_web_service_furtherfields', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Publication'])),
        ))
        db.send_create_signal('core_web_service', ['FurtherFields'])

        # Adding model 'PeerReviewTemplates'
        db.create_table('core_web_service_peerreviewtemplates', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template_text', self.gf('django.db.models.fields.TextField')()),
            ('template_binary_path', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal('core_web_service', ['PeerReviewTemplates'])

        # Adding model 'PeerReview'
        db.create_table('core_web_service_peerreview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('peer_reviewer', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Publication'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.PeerReviewTemplates'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('review', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core_web_service', ['PeerReview'])

        # Adding model 'Rating'
        db.create_table('core_web_service_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Publication'])),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
        ))
        db.send_create_signal('core_web_service', ['Rating'])

        # Adding model 'ReferenceMaterial'
        db.create_table('core_web_service_referencematerial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Publication'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core_web_service', ['ReferenceMaterial'])


    def backwards(self, orm):
        
        # Deleting model 'Author'
        db.delete_table('core_web_service_author')

        # Deleting model 'Vote'
        db.delete_table('core_web_service_vote')

        # Deleting model 'Tag'
        db.delete_table('core_web_service_tag')

        # Deleting model 'Comment'
        db.delete_table('core_web_service_comment')

        # Deleting model 'Esteem'
        db.delete_table('core_web_service_esteem')

        # Deleting model 'Publication'
        db.delete_table('core_web_service_publication')

        # Removing M2M table for field authors on 'Publication'
        db.delete_table('core_web_service_publication_authors')

        # Removing M2M table for field comments on 'Publication'
        db.delete_table('core_web_service_publication_comments')

        # Removing M2M table for field tags on 'Publication'
        db.delete_table('core_web_service_publication_tags')

        # Deleting model 'FurtherFields'
        db.delete_table('core_web_service_furtherfields')

        # Deleting model 'PeerReviewTemplates'
        db.delete_table('core_web_service_peerreviewtemplates')

        # Deleting model 'PeerReview'
        db.delete_table('core_web_service_peerreview')

        # Deleting model 'Rating'
        db.delete_table('core_web_service_rating')

        # Deleting model 'ReferenceMaterial'
        db.delete_table('core_web_service_referencematerial')


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
            'User': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Tag']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'core_web_service.furtherfields': {
            'Meta': {'object_name': 'FurtherFields'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Publication']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'core_web_service.peerreview': {
            'Meta': {'object_name': 'PeerReview'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peer_reviewer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Publication']"}),
            'review': ('django.db.models.fields.TextField', [], {}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.PeerReviewTemplates']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core_web_service.peerreviewtemplates': {
            'Meta': {'object_name': 'PeerReviewTemplates'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template_binary_path': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'template_text': ('django.db.models.fields.TextField', [], {})
        },
        'core_web_service.publication': {
            'Meta': {'object_name': 'Publication'},
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
            'month': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publication_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        },
        'core_web_service.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['core_web_service']
