# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('parameter_value', models.TextField()),
            ],
            options={
                'db_table': 'answer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'attribute',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=50)),
                ('attr', models.ForeignKey(to='ExpertSystem.Attribute')),
            ],
            options={
                'db_table': 'attribute_value',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'parameter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParameterValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=50)),
                ('param', models.ForeignKey(to='ExpertSystem.Parameter')),
            ],
            options={
                'db_table': 'parameter_value',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('type', models.IntegerField(choices=[(0, b'\xd0\x92\xd1\x8b\xd0\xb1\xd0\xb5\xd1\x80\xd0\xb8\xd1\x82\xd0\xb5 \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82'), (1, b'\xd0\x9d\xd0\xb0\xd0\xbf\xd0\xb8\xd1\x88\xd0\xb8\xd1\x82\xd0\xb5 \xd1\x87\xd0\xb8\xd1\x81\xd0\xbb\xd0\xbe')])),
                ('parameter', models.ForeignKey(to='ExpertSystem.Parameter')),
            ],
            options={
                'db_table': 'question',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condition', models.TextField()),
                ('result', models.TextField()),
                ('type', models.IntegerField(choices=[(0, b'\xd0\x9f\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd0\xbb\xd0\xbe \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xbf\xd0\xb0\xd1\x80\xd0\xb0\xd0\xbc\xd0\xb5\xd1\x82\xd1\x80\xd0\xb0'), (1, b'\xd0\x9f\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd0\xbb\xd0\xbe \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xb0\xd1\x82\xd1\x80\xd0\xb8\xd0\xb1\xd1\x83\xd1\x82\xd0\xb0')])),
            ],
            options={
                'db_table': 'rule',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SysObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('attributes', models.ManyToManyField(related_name=b'sys_objects', null=True, to='ExpertSystem.AttributeValue', blank=True)),
            ],
            options={
                'db_table': 'sys_object',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'system',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sysobject',
            name='system',
            field=models.ForeignKey(to='ExpertSystem.System'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='system',
            field=models.ForeignKey(to='ExpertSystem.System'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parametervalue',
            name='system',
            field=models.ForeignKey(to='ExpertSystem.System'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parameter',
            name='system',
            field=models.ForeignKey(to='ExpertSystem.System'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='system',
            field=models.ForeignKey(to='ExpertSystem.System'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='system',
            field=models.ForeignKey(to='ExpertSystem.System'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='ExpertSystem.Question'),
            preserve_default=True,
        ),
    ]
