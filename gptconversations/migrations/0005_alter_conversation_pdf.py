# Generated by Django 5.1.2 on 2024-10-22 08:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gptconversations", "0004_conversation_pdf"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conversation",
            name="pdf",
            field=models.FileField(blank=True, default="", null=True, upload_to=""),
        ),
    ]
