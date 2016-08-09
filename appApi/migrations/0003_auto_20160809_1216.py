# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appApi', '0002_smsmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('android_version', models.CharField(max_length=128)),
                ('android_url', models.CharField(max_length=128)),
                ('android_notes', models.CharField(max_length=128)),
                ('android_radio', models.IntegerField()),
            ],
            options={
                'db_table': 'config',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='user',
            name='community',
            field=models.ForeignKey(on_delete=None, blank=True, to='appApi.Community', null=True),
            preserve_default=True,
        ),
    ]
