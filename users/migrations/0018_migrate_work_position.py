from __future__ import unicode_literals

from django.db import migrations


def forward(apps, schema_editor):
    UserProfile = apps.get_model("users", "UserProfile")
    for up in UserProfile.objects.all():
        if up.work:
            up.works.add(up.work)
        if up.position:
            up.positions.add(up.position)

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20170516_1910'),
    ]

    operations = [
        migrations.RunPython(forward)
    ]
