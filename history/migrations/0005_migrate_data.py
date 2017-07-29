from django.db import migrations


def forward(apps, schema_editor):
    History = apps.get_model("history", "PollHistory")
    GroupHistory = apps.get_model("history", "GroupHistory")
    for history in History.objects.all():
        h1 = GroupHistory(group=history.user_group, history=history, date_created=history.date_modified)
        h1.save()


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_auto_20170515_1043'),
    ]

    operations = [
        migrations.RunPython(forward)
]