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
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=75, db_index=True)),
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
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core_web_service', ['Esteem'])

        # Adding model 'Keyword'
        db.create_table('core_web_service_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('core_web_service', ['Keyword'])

        # Adding model 'Rating'
        db.create_table('core_web_service_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('votes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core_web_service', ['Rating'])

        # Adding model 'Publication'
        db.create_table('core_web_service_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(blank=True)),
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
            ('review_status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('publication_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rating', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core_web_service.Rating'], unique=True)),
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

        # Adding M2M table for field keywords on 'Publication'
        db.create_table('core_web_service_publication_keywords', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publication', models.ForeignKey(orm['core_web_service.publication'], null=False)),
            ('keyword', models.ForeignKey(orm['core_web_service.keyword'], null=False))
        ))
        db.create_unique('core_web_service_publication_keywords', ['publication_id', 'keyword_id'])

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

        # Adding model 'ResearchArea'
        db.create_table('core_web_service_researcharea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('core_web_service', ['ResearchArea'])

        # Adding model 'UserProfile'
        db.create_table('core_web_service_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('authenticated_professional', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('core_web_service', ['UserProfile'])

        # Adding M2M table for field research_areas on 'UserProfile'
        db.create_table('core_web_service_userprofile_research_areas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['core_web_service.userprofile'], null=False)),
            ('researcharea', models.ForeignKey(orm['core_web_service.researcharea'], null=False))
        ))
        db.create_unique('core_web_service_userprofile_research_areas', ['userprofile_id', 'researcharea_id'])

        # Adding model 'ProfileField'
        db.create_table('core_web_service_profilefield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.UserProfile'])),
        ))
        db.send_create_signal('core_web_service', ['ProfileField'])

        # Adding model 'FurtherField'
        db.create_table('core_web_service_furtherfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Publication'])),
        ))
        db.send_create_signal('core_web_service', ['FurtherField'])

        # Adding model 'PeerReviewTemplate'
        db.create_table('core_web_service_peerreviewtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template_text', self.gf('django.db.models.fields.TextField')()),
            ('template_binary_path', self.gf('django.db.models.fields.CharField')(max_length=4096)),
        ))
        db.send_create_signal('core_web_service', ['PeerReviewTemplate'])

        # Adding model 'PeerReview'
        db.create_table('core_web_service_peerreview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('peer_reviewer', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('publication', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.Publication'])),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core_web_service.PeerReviewTemplate'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('review', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('core_web_service', ['PeerReview'])

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

        # Deleting model 'Keyword'
        db.delete_table('core_web_service_keyword')

        # Deleting model 'Rating'
        db.delete_table('core_web_service_rating')

        # Deleting model 'Publication'
        db.delete_table('core_web_service_publication')

        # Removing M2M table for field authors on 'Publication'
        db.delete_table('core_web_service_publication_authors')

        # Removing M2M table for field comments on 'Publication'
        db.delete_table('core_web_service_publication_comments')

        # Removing M2M table for field tags on 'Publication'
        db.delete_table('core_web_service_publication_tags')

        # Removing M2M table for field keywords on 'Publication'
        db.delete_table('core_web_service_publication_keywords')

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

        # Deleting model 'ResearchArea'
        db.delete_table('core_web_service_researcharea')

        # Deleting model 'UserProfile'
        db.delete_table('core_web_service_userprofile')

        # Removing M2M table for field research_areas on 'UserProfile'
        db.delete_table('core_web_service_userprofile_research_areas')

        # Deleting model 'ProfileField'
        db.delete_table('core_web_service_profilefield')

        # Deleting model 'FurtherField'
        db.delete_table('core_web_service_furtherfield')

        # Deleting model 'PeerReviewTemplate'
        db.delete_table('core_web_service_peerreviewtemplate')

        # Deleting model 'PeerReview'
        db.delete_table('core_web_service_peerreview')

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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'core_web_service.furtherfield': {
            'Meta': {'object_name': 'FurtherField'},
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
        'core_web_service.profilefield': {
            'Meta': {'object_name': 'ProfileField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.UserProfile']"}),
            'value': ('django.db.models.fields.TextField', [], {})
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
            'rating': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core_web_service.Rating']", 'unique': 'True'}),
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
            'rating': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        },
        'core_web_service.referencematerial': {
            'Meta': {'object_name': 'ReferenceMaterial'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'publication': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core_web_service.Publication']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core_web_service.researcharea': {
            'Meta': {'object_name': 'ResearchArea'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'research_areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core_web_service.ResearchArea']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'core_web_service.vote': {
            'Meta': {'object_name': 'Vote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['core_web_service']
