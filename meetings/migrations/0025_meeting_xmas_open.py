# Generated by Django 2.2.24 on 2021-11-27 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0024_auto_20210318_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='xmas_open',
            field=models.BooleanField(default=False),
        ),
    ]
