# Generated by Django 2.2.16 on 2020-11-14 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0017_auto_20201114_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='types',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
