# Generated by Django 4.2.4 on 2023-10-10 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("messenger", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="messengerroom",
            name="admin_room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="admin_room",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Админ чата",
            ),
        ),
        migrations.AddField(
            model_name="messengerroom",
            name="participants",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="message",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="room_m",
                to="messenger.messengerroom",
                verbose_name="Комната чата",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="message_author",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор сообщения",
            ),
        ),
    ]
