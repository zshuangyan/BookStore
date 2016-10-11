# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20160928_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sex', models.IntegerField(choices=[(1, 'male'), (2, 'female')], default=1)),
                ('birth', models.DateField()),
                ('age', models.IntegerField()),
                ('company', models.CharField(max_length=120)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
        ),
    ]
