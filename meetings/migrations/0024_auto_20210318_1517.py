# Generated by Django 2.2.19 on 2021-03-18 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0023_emailcontact'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='gso_opt_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='sub_types',
            field=models.ManyToManyField(blank=True, related_name='meeting_categories', to='meetings.MeetingSubType'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='submission',
            field=models.CharField(choices=[('new', 'new'), ('existing', 'existing')], default='existing', max_length=10),
        ),
    ]
