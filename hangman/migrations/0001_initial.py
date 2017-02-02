# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HangmanWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=32)),
                ('word', models.CharField(max_length=200)),
                ('word_so_far', models.CharField(max_length=200)),
                ('wrong_letters', models.CharField(max_length=200)),
            ],
        ),
    ]