# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-05 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('test_models', '0008_mystatisticalmodel_has_results'),
    ]

    operations = [
        migrations.CreateModel(
            name='MySupervisedLearningTechnique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('engine_object', picklefield.fields.PickledObjectField(blank=True, editable=False, null=True, verbose_name='Engine Object')),
                ('engine_object_timestamp', models.DateTimeField(blank=True, null=True, verbose_name='Engine Object Timestamp')),
                ('sm_type', models.SmallIntegerField(blank=True, choices=[(0, 'General'), (1, 'Classification'), (2, 'Regression')], default=0, null=True, verbose_name='Statistical Technique Type')),
                ('metadata', jsonfield.fields.JSONField(blank=True, default={}, null=True, verbose_name='Metadata')),
                ('engine_meta_iterations', models.SmallIntegerField(default=1, verbose_name='Engine Meta Iterations')),
                ('engine_iterations', models.SmallIntegerField(blank=True, null=True, verbose_name='Engine Iterations (Max)')),
                ('has_results', models.BooleanField(default=True, verbose_name='Has Results?')),
                ('results_storage', models.CharField(blank=True, max_length=100, null=True, verbose_name='Results Storage')),
                ('counter', models.IntegerField(blank=True, default=0, null=True, verbose_name='Internal Counter')),
                ('counter_threshold', models.IntegerField(blank=True, null=True, verbose_name='Internal Counter Threshold')),
                ('threshold_actions', models.CharField(blank=True, max_length=200, null=True, verbose_name='Threshold actions')),
                ('sl_type', models.SmallIntegerField(blank=True, choices=[(0, 'Classification'), (1, 'Regression')], default=0, null=True, verbose_name='Supervised Learning Type')),
                ('labels_column', models.CharField(blank=True, help_text='Format: app_label.model.attribute', max_length=100, null=True, verbose_name="Labels' Column")),
            ],
        ),
    ]
