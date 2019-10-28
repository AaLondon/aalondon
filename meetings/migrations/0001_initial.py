# Generated by Django 2.2.6 on 2019-10-28 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=300)),
                ('code', models.IntegerField()),
                ('day', models.TextField(max_length=10)),
                ('hearing', models.BooleanField()),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('postcode', models.TextField(max_length=10)),
                ('time', models.TimeField()),
                ('duration', models.TextField(max_length=20)),
                ('title', models.TextField()),
                ('wheelchair', models.BooleanField()),
            ],
        ),
    ]
