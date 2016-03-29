# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expdatetime',
            field=models.DateTimeField(default=b'2015-04-27 18:33:47.277000'),
        ),
    ]
