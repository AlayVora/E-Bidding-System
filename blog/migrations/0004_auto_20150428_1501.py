# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150427_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='BIDFORYOU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_id', models.IntegerField()),
                ('bid_value', models.IntegerField()),
                ('bidder_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='expdatetime',
            field=models.DateTimeField(default=b'2015-04-28 16:01:10.227000'),
        ),
    ]
