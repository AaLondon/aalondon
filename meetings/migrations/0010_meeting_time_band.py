# Generated by Django 2.2.9 on 2020-06-13 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_auto_20200203_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='time_band',
            field=models.CharField(max_length=10, null=True),
        ),
    ]