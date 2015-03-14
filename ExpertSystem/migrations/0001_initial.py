# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'System'
        db.create_table('system', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'ExpertSystem', ['System'])

        # Adding model 'Attribute'
        db.create_table('attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.System'])),
        ))
        db.send_create_signal(u'ExpertSystem', ['Attribute'])

        # Adding model 'Parameter'
        db.create_table('parameter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.System'])),
        ))
        db.send_create_signal(u'ExpertSystem', ['Parameter'])

        # Adding model 'Question'
        db.create_table('question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.Parameter'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.System'])),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ExpertSystem', ['Question'])

        # Adding model 'ParameterValue'
        db.create_table('parameter_value', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.System'])),
            ('param', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.Parameter'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'ExpertSystem', ['ParameterValue'])

        # Adding model 'Answer'
        db.create_table('answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['ExpertSystem.Question'])),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('parameter_value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'ExpertSystem', ['Answer'])

        # Adding model 'AttributeValue'
        db.create_table('attribute_value', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.System'])),
            ('attr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.Attribute'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'ExpertSystem', ['AttributeValue'])

        # Adding model 'SysObject'
        db.create_table('sys_object', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.System'])),
        ))
        db.send_create_signal(u'ExpertSystem', ['SysObject'])

        # Adding M2M table for field attributes on 'SysObject'
        m2m_table_name = db.shorten_name('sys_object_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sysobject', models.ForeignKey(orm[u'ExpertSystem.sysobject'], null=False)),
            ('attributevalue', models.ForeignKey(orm[u'ExpertSystem.attributevalue'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sysobject_id', 'attributevalue_id'])

        # Adding model 'Rule'
        db.create_table('rule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condition', self.gf('django.db.models.fields.TextField')()),
            ('result', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ExpertSystem.System'])),
        ))
        db.send_create_signal(u'ExpertSystem', ['Rule'])


    def backwards(self, orm):
        # Deleting model 'System'
        db.delete_table('system')

        # Deleting model 'Attribute'
        db.delete_table('attribute')

        # Deleting model 'Parameter'
        db.delete_table('parameter')

        # Deleting model 'Question'
        db.delete_table('question')

        # Deleting model 'ParameterValue'
        db.delete_table('parameter_value')

        # Deleting model 'Answer'
        db.delete_table('answer')

        # Deleting model 'AttributeValue'
        db.delete_table('attribute_value')

        # Deleting model 'SysObject'
        db.delete_table('sys_object')

        # Removing M2M table for field attributes on 'SysObject'
        db.delete_table(db.shorten_name('sys_object_attributes'))

        # Deleting model 'Rule'
        db.delete_table('rule')


    models = {
        u'ExpertSystem.answer': {
            'Meta': {'object_name': 'Answer', 'db_table': "'answer'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter_value': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['ExpertSystem.Question']"})
        },
        u'ExpertSystem.attribute': {
            'Meta': {'object_name': 'Attribute', 'db_table': "'attribute'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.System']"})
        },
        u'ExpertSystem.attributevalue': {
            'Meta': {'object_name': 'AttributeValue', 'db_table': "'attribute_value'"},
            'attr': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.Attribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.System']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'ExpertSystem.parameter': {
            'Meta': {'object_name': 'Parameter', 'db_table': "'parameter'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.System']"})
        },
        u'ExpertSystem.parametervalue': {
            'Meta': {'object_name': 'ParameterValue', 'db_table': "'parameter_value'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'param': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.Parameter']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.System']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'ExpertSystem.question': {
            'Meta': {'object_name': 'Question', 'db_table': "'question'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.Parameter']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.System']"}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ExpertSystem.rule': {
            'Meta': {'object_name': 'Rule', 'db_table': "'rule'"},
            'condition': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.System']"}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ExpertSystem.sysobject': {
            'Meta': {'object_name': 'SysObject', 'db_table': "'sys_object'"},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sys_objects'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['ExpertSystem.AttributeValue']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ExpertSystem.System']"})
        },
        u'ExpertSystem.system': {
            'Meta': {'object_name': 'System', 'db_table': "'system'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
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
        }
    }

    complete_apps = ['ExpertSystem']