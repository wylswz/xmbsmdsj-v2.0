# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-26 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_photo_exif'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='author',
            field=models.CharField(default='Y.WEN', max_length=400),
        ),
    ]
