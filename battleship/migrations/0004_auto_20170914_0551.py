# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0003_auto_20170914_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='appID',
            field=models.CharField(default='', max_length=30),
        ),
    ]
