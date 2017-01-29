# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('spc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Rules',
        ),
        migrations.AlterField(
            model_name='user',
            name='login_trackmania',
            field=models.CharField(max_length=64),
        ),
    ]
