# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-18 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0007_queue_opponent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queue',
            name='opponent',
            field=models.CharField(default='', max_length=30),
        ),
    ]
