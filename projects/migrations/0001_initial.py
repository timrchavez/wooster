# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DependencyType'
        db.create_table(u'projects_dependencytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('config_xml', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'projects', ['DependencyType'])

        # Adding model 'Dependency'
        db.create_table(u'projects_dependency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('dependency_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.DependencyType'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jenkins.Job'], null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['Dependency'])

        # Adding model 'ProjectDependency'
        db.create_table(u'projects_projectdependency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dependency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Dependency'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('auto_track', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('current_build', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jenkins.Build'], null=True)),
        ))
        db.send_create_signal(u'projects', ['ProjectDependency'])

        # Adding model 'Project'
        db.create_table(u'projects_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'projects', ['Project'])

        # Adding model 'ProjectBuild'
        db.create_table(u'projects_projectbuild', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('requested_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('requested_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='INCOMPLETE', max_length=10)),
            ('build_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'projects', ['ProjectBuild'])

        # Adding model 'ProjectBuildDependency'
        db.create_table(u'projects_projectbuilddependency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'projects', ['ProjectBuildDependency'])


    def backwards(self, orm):
        # Deleting model 'DependencyType'
        db.delete_table(u'projects_dependencytype')

        # Deleting model 'Dependency'
        db.delete_table(u'projects_dependency')

        # Deleting model 'ProjectDependency'
        db.delete_table(u'projects_projectdependency')

        # Deleting model 'Project'
        db.delete_table(u'projects_project')

        # Deleting model 'ProjectBuild'
        db.delete_table(u'projects_projectbuild')

        # Deleting model 'ProjectBuildDependency'
        db.delete_table(u'projects_projectbuilddependency')


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
        u'jenkins.build': {
            'Meta': {'ordering': "['-number']", 'object_name': 'Build'},
            'build_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jenkins.Job']"}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'phase': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'jenkins.jenkinsserver': {
            'Meta': {'object_name': 'JenkinsServer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'remote_addr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'jenkins.job': {
            'Meta': {'object_name': 'Job'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jenkins.JenkinsServer']"})
        },
        u'projects.dependency': {
            'Meta': {'object_name': 'Dependency'},
            'dependency_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.DependencyType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jenkins.Job']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'projects.dependencytype': {
            'Meta': {'object_name': 'DependencyType'},
            'config_xml': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.Dependency']", 'through': u"orm['projects.ProjectDependency']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.projectbuild': {
            'Meta': {'object_name': 'ProjectBuild'},
            'build_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'requested_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'requested_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'INCOMPLETE'", 'max_length': '10'})
        },
        u'projects.projectbuilddependency': {
            'Meta': {'object_name': 'ProjectBuildDependency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.projectdependency': {
            'Meta': {'object_name': 'ProjectDependency'},
            'auto_track': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'current_build': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jenkins.Build']", 'null': 'True'}),
            'dependency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Dependency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"})
        }
    }

    complete_apps = ['projects']