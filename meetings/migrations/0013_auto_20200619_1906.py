# Generated by Django 2.2.9 on 2020-06-19 19:06

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0012_auto_20200619_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=100, populate_from=['title', 'day', 'postcode']),
        ),
    ]
