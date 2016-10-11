# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_useraddress_is_default'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraddress',
            old_name='is_default',
            new_name='default',
        ),
    ]
