# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        ('order', '0002_order_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('Order', models.ForeignKey(to='order.Order', related_name='items')),
                ('book', models.ForeignKey(to='catalog.Book')),
            ],
        ),
    ]
