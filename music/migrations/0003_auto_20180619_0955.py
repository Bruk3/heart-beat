# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-06-19 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20180619_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='pushed_to',
            field=models.CharField(choices=[(1, 'bruk'), (2, 'abebe'), (3, 'chala')], default=0, max_length=1),
        ),
    ]
