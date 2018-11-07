# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import magazine.models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0002_auto_20170228_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='cover_image',
            field=models.ImageField(null=True, upload_to=magazine.models.issue_upload_to, blank=True),
        ),
    ]
