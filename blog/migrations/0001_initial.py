# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CATEGORY',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PRODUCT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=100)),
                ('product_desc', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('product_path', models.CharField(max_length=200)),
                ('owner', models.IntegerField()),
                ('status', models.PositiveSmallIntegerField(default=1)),
                ('expdatetime', models.DateTimeField(default=b'2015-04-25 14:24:43.354000')),
                ('category_id', models.ForeignKey(to='blog.CATEGORY')),
            ],
        ),
        migrations.CreateModel(
            name='SOLD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_id', models.IntegerField()),
                ('bid_value', models.IntegerField()),
                ('old_owner', models.IntegerField()),
                ('new_owner', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TRANSACT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bidder_id', models.IntegerField()),
                ('bid_value', models.IntegerField(default=1)),
                ('product', models.ForeignKey(to='blog.PRODUCT')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card_no', models.CharField(max_length=16, null=True)),
                ('exp_date', models.DateField(null=True)),
                ('cvv', models.CharField(max_length=3, null=True)),
                ('bids', models.PositiveSmallIntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
