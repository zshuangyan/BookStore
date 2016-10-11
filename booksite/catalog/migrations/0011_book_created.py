# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20160919_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='created',
            field=models.DateField(null=True),
        ),
    ]
