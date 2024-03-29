# Generated by Django 3.2.16 on 2023-09-06 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0038_alter_meeting_email_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='temporary_changes',
            field=models.TextField(blank=True, default='', help_text='e.g. Please note that this meeting is closed on this day.', max_length=1000),
        ),
    ]
