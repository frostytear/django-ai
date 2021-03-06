# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-13 08:02
from __future__ import unicode_literals
import os
import tarfile
import urllib.request
import random
import zipfile
import csv
import io

from django.db import migrations, models


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENRON_MAILS_FILE_NAME = os.path.join(CURRENT_DIR, "enron1.tar.gz")
ENRON_MAILS_FILE_URL = ("http://www.aueb.gr/users/ion/data/enron-spam/"
                        "preprocessed/enron1.tar.gz")
YOUTUBE_COMMENTS_FILE_NAME = os.path.join(CURRENT_DIR,
                                          "YouTube-Spam-Collection-v1.zip")
YOUTUBE_COMMENTS_FILE_URL = ("https://archive.ics.uci.edu/ml/"
                             "machine-learning-databases/00380/"
                             "YouTube-Spam-Collection-v1.zip")


def confirm(question):
    """
    https://gist.github.com/garrettdreyfus/8153571
    """
    reply = str(input(' -> ' + question + ' (Y/n): ')).lower().strip()
    if reply == 'y' or reply == '':
        return True
    elif reply == 'n':
        return False
    else:
        return confirm("Mmmm... Please enter")


def download_and_process_pretrain_data_files(apps, schema_editor):
    """
    Forward Operation: Downloads if neccesary the sample data and populates
    Pre-Train Models.
    """
    SFPTEnron = apps.get_model("examples", "SFPTEnron")
    SFPTYoutube = apps.get_model("examples", "SFPTYoutube")
    random.seed(1234567)

    # -> Download datasets if not exist
    if (not os.path.exists(ENRON_MAILS_FILE_NAME) or
            not os.path.exists(YOUTUBE_COMMENTS_FILE_NAME)):
        if confirm("Proceed to download pre-training datasets?"):
            if not os.path.exists(ENRON_MAILS_FILE_NAME):
                print("    Downloading Enron mails dataset...")
                urllib.request.urlretrieve(
                    ENRON_MAILS_FILE_URL,
                    ENRON_MAILS_FILE_NAME
                )
            if not os.path.exists(YOUTUBE_COMMENTS_FILE_NAME):
                print("     Downloading Youtube comments dataset...")
                urllib.request.urlretrieve(
                    YOUTUBE_COMMENTS_FILE_URL,
                    YOUTUBE_COMMENTS_FILE_NAME
                )
    # -> Process the Enron mails file
    with tarfile.open(name=ENRON_MAILS_FILE_NAME, mode="r:gz") as tfile:
        for member in tfile.getmembers():
            if member.isfile() and "Summary" not in member.name:
                message = tfile.extractfile(member).read()
                SFPTEnron.objects.create(
                    content=message.decode('raw_unicode_escape'),
                    is_spam=("spam" in member.name),
                )
    # -> Process Youtube comments file
    with zipfile.ZipFile(YOUTUBE_COMMENTS_FILE_NAME) as zfile:
        yt_files = [file for file in zfile.filelist
                    if "MACOSX" not in file.filename]
        for yt_file in yt_files:
            with zfile.open(yt_file.filename) as csvfile:
                csvfile_sio = io.StringIO(
                    csvfile.read().decode('raw_unicode_escape')
                )
                reader = csv.DictReader(csvfile_sio)
                for row in reader:
                    SFPTYoutube.objects.create(
                        content=row['CONTENT'],
                        is_spam=(row['CLASS'] == '1')
                    )


def confirm_deletion_pretrain_data_files(apps, schema_editor):
    """
    Backward Operation: Remove the file if deemed necessary, no need to remove
    the objects as the table will be removed.
    """
    if not confirm(
            "Leave downloaded pre-train datasets files for the future?"):
        os.remove(ENRON_MAILS_FILE_NAME)
        os.remove(YOUTUBE_COMMENTS_FILE_NAME)


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0014_missing_ui_meta'),
    ]

    operations = [
        migrations.CreateModel(
            name='SFPTEnron',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('is_spam', models.BooleanField(
                    default=False, verbose_name='Is Spam?')),
            ],
            options={
                'verbose_name': 'Spam Filter Pre-training: Enron Email Data',
                'verbose_name_plural': ('Spam Filter Pre-trainings: '
                                        'Enron Emails Data'),
            },
        ),
        migrations.CreateModel(
            name='SFPTYoutube',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('is_spam', models.BooleanField(
                    default=False, verbose_name='Is Spam?')),
            ],
            options={
                'verbose_name': ('Spam Filter Pre-training: '
                                 'Youtube Comment Data'),
                'verbose_name_plural': ('Spam Filter Pre-trainings: '
                                        'Youtube Comments Data'),
            },
        ),
        migrations.RunPython(
            download_and_process_pretrain_data_files,
            confirm_deletion_pretrain_data_files
        ),

    ]
