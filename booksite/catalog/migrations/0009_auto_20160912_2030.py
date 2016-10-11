# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20160912_2022'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='categories',
            new_name='category',
        ),
    ]
