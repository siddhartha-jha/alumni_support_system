# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170328_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(upload_to=core.models.get_image_path, default='/media/users/default_avatar.jpeg'),
        ),
    ]
