# Generated by Django 3.2.16 on 2022-12-28 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0026_meeting_xmas_closed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='payment_details',
            new_name='tradition_7_details',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='conference_url',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='covid_open_status',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='hearing',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='intergroup_id',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='types',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='wheelchair',
        ),
        migrations.AddField(
            model_name='meeting',
            name='postcode_prefix',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
