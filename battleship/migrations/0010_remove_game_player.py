# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-18 16:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0009_auto_20170918_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='player',
        ),
    ]
