# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20170329_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='batch',
            field=models.CharField(blank=True, choices=[('NA', 'Not Applicable'), (1998, '1998'), (1999, '1999'), (2000, '2000'), (2001, '2001'), (2002, '2002'), (2003, '2003'), (2004, '2004'), (2005, '2005'), (2006, '2006'), (2007, '2007'), (2008, '2008'), (2009, '2009'), (2010, '2010'), (2011, '2011'), (2012, '2012'), (2013, '2013'), (2014, '2014')], max_length=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(default='C:\\Users\\siddh_000\\documents\\visual studio 2015\\Projects\\alumni_support_system\\alumni_support_system\\media\\users\\default_avatar.jpeg', upload_to=core.models.get_image_path),
        ),
    ]
