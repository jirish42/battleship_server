# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0004_auto_20170914_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='gameID',
            field=models.CharField(default='', max_length=30),
        ),
    ]
