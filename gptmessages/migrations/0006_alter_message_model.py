# Generated by Django 5.1.2 on 2024-10-23 13:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gptmessages", "0005_alter_message_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="model",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
    ]
