# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20160912_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(null=True, upload_to='img/books/'),
        ),
        migrations.AddField(
            model_name='book',
            name='img_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
