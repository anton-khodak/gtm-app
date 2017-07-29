from django.db import migrations


def forward(apps, schema_editor):
    History = apps.get_model("history", "PollHistory")
    # GroupHistory = apps.get_model("history", "GroupHistory")
    for history in History.objects.all():
        history.groups.add(history.user_group)


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0008_auto_20170515_1455'),
    ]

    operations = [
        migrations.RunPython(forward)
]