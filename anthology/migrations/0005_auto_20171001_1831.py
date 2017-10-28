# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anthology', '0004_content_subsection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='subsection',
            field=models.IntegerField(default=0),
        ),
    ]
