# Generated by Django 2.2.16 on 2020-11-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0016_meeting_intergroup_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='group',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='group_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]