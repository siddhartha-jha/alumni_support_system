# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170330_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(default='users\\default_avatar.jpg', upload_to=core.models.get_image_path),
        ),
    ]
