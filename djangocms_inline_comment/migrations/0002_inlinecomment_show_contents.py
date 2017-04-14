# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_inline_comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inlinecomment',
            name='show_contents',
            field=models.BooleanField(default=False, verbose_name='Show Contents'),
        ),
    ]
