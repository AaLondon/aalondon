from django.db import migrations, models


def add_event_types(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return
    EventType = apps.get_model('event','EventType')
    event_types = ['Convention','Region','Workshop','Intergroup']
    for incoming_type in event_types:
        obj,created = EventType.objects.get_or_create(value=incoming_type)
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200220_1633'),
    ]

    operations = [ migrations.RunPython(add_event_types),
    ]
