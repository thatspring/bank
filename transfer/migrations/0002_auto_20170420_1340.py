# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessrecord',
            name='transferID',
            field=models.CharField(default='000000000000000000000000', max_length=24, unique=True),
        ),
        migrations.AlterField(
            model_name='businessrecord',
            name='user',
            field=models.CharField(max_length=16),
        ),
    ]
