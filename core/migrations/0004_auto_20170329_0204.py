# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170329_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(default='C:/Users/siddh_000/Documents/Visual Studio 2015/Projects/alumni_support_system/alumni_support_system/media/users/default_avatar.jpeg', upload_to=core.models.get_image_path),
        ),
    ]
