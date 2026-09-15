from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_dan(apps, schema_editor):
    User = apps.get_model("auth", "User")
    if not User.objects.filter(username="dan").exists():
        User.objects.create(
            username="dan",
            password=make_password("Optimization1234"),
            is_staff=True,
            is_superuser=True,
        )


def remove_dan(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="dan").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_dan, remove_dan),
    ]