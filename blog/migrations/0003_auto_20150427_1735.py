# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150427_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expdatetime',
            field=models.DateTimeField(default=b'2015-04-27 18:35:56.982000'),
        ),
    ]
