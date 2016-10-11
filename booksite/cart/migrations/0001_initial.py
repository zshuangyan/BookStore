# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('cart_id', models.CharField(max_length=32)),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(to='catalog.Book')),
            ],
        ),
    ]
