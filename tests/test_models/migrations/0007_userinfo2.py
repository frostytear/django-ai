# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-04 05:32
from __future__ import unicode_literals

import numpy as np

from django.db import migrations, models


def populate_userinfos2(apps, schema_editor):
    UserInfo2 = apps.get_model("test_models", "UserInfo2")
    # Use a fixed seed for generate content
    np.random.seed(123456)
    # Size of table
    size = 100
    # Average 2 is a metric normally distributed around 20 with a std dev of 5
    avg2 = np.random.normal(20, 5, size=(size,))
    # Average Times spent on Pages B is a metric normally distributed around
    # 30 with a std dev of 5
    avg_time_pages_b = np.random.normal(30, 5, size=(size,))
    # Create the objects in the Model
    uis = []
    for i in range(0, size):
        uis.append(UserInfo2(avg_time_pages_b=avg_time_pages_b[i],
                             avg2=avg2[i]))
    UserInfo2.objects.bulk_create(uis)


def unpopuplate_userinfos2(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('test_models', '0006_create_mystatmodel_and_alter_ui_avg_time_pages'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo2',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('avg2', models.FloatField(
                    blank=True, null=True, verbose_name='Average 2')),
                ('avg_time_pages_b', models.FloatField(
                    blank=True, null=True,
                    verbose_name='Average Time spent on Pages B')),
                ('cluster_2', models.CharField(
                    blank=True, max_length=1, null=True,
                    verbose_name='Cluster 1')),
            ],
        ),
        migrations.RunPython(populate_userinfos2,
                             unpopuplate_userinfos2),
    ]
