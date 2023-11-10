# Generated by Django 4.2.4 on 2023-10-10 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["-timestamp"],
            },
        ),
        migrations.CreateModel(
            name="MessengerRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=128, null=True, unique=True
                    ),
                ),
                (
                    "room_type",
                    models.CharField(
                        choices=[("dr", "direct_room"), ("cr", "common_room")],
                        default="dr",
                        max_length=2,
                    ),
                ),
                ("slug", models.SlugField(max_length=40, unique=True)),
            ],
            options={
                "verbose_name": "Чат-комната",
                "verbose_name_plural": "Чат-комнаты",
            },
        ),
    ]
