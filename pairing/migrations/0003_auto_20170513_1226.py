# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pairing', '0002_auto_20170513_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='game',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='standing',
            name='game',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Round',
        ),
    ]