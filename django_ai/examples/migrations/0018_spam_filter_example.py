# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-12 15:26
from __future__ import unicode_literals

from django.db import migrations


def create_spam_filter_example(apps, schema_editor):
    # import ipdb; ipdb.set_trace()
    SpamFilter = apps.get_model(
        "spam_filtering", "SpamFilter")
    SVC = apps.get_model(
        "supervised_learning", "SVC")
    DataColumn = apps.get_model(
        "base", "DataColumn")
    ContentType = apps.get_model(
        "contenttypes", "ContentType")

    svm = SVC(
        name="SVM for Spam (example)",
        kernel="linear",
        penalty_parameter=0.1,
    )
    svm.save()
    sf = SpamFilter(
        name="Spam Filter for Comments (example)",
        classifier="supervised_learning.SVC|SVM for Spam (example)",
        counter_threshold=5,
        counter_threshold_actions=":recalculate",
        spam_model_is_enabled=True,
        spam_model_model="examples.CommentOfMySite",
        labels_column="examples.commentofmysite.is_spam",
        pretraining="examples.SFPTYoutube",
        cv_is_enabled=True,
        cv_folds=10,
        cv_metric="average_precision",
        bow_is_enabled=True,
        bow_analyzer="word",
        bow_ngram_range_min=1,
        bow_ngram_range_max=3,
        bow_max_df=0.9,
        bow_min_df=0.001
    )
    sf.save()
    dc = DataColumn(
        content_type=ContentType.objects.get(model="spamfilter",
                                             app_label="spam_filtering"),
        object_id=sf.id,
        ref_model=ContentType.objects.get(model="commentofmysite",
                                          app_label="examples"),
        ref_column="comment",
        position=0
    )
    dc.save()


def delete_spam_filter_example(apps, schema_editor):
    SpamFilter = apps.get_model(
        "spam_filtering", "SpamFilter")
    SVC = apps.get_model(
        "supervised_learning", "SVC")

    SVC.objects.get(name="SVM for Spam (example)").delete()
    SpamFilter.objects.get(name="Spam Filter for Comments (example)").delete()
    # DataColumn should be deleted on models.CASCADE


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0017_nullboolean_for_coms_is_spam'),
    ]

    operations = [
        migrations.RunPython(
            create_spam_filter_example,
            delete_spam_filter_example
        )
    ]
