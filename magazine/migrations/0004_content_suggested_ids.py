# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0003_auto_20171001_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='suggested_ids',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
