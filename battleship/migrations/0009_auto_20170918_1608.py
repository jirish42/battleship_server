# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-18 16:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battleship', '0008_auto_20170918_0512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='player1',
            new_name='player',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player2',
        ),
    ]