# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0006_auto_20170914_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='opponent',
            field=models.BooleanField(default=False),
        ),
    ]
