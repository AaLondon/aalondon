# Generated by Django 3.2.16 on 2022-12-28 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0027_auto_20221228_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='gso_opt_in',
            new_name='gso_opt_out',
        ),
    ]
