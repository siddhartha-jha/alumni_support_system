# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('bio', models.TextField(blank=True, max_length=500, default='')),
                ('city', models.CharField(blank=True, max_length=30, default='')),
                ('birth_date', models.DateField(blank=True, null=True, default='9999-12-31')),
                ('website', models.URLField(blank=True, default='')),
                ('organization', models.CharField(blank=True, max_length=100, default='')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
