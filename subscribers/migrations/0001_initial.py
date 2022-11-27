# Generated by Django 4.1.3 on 2022-11-25 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subscriber",
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
                    "first_name",
                    models.CharField(help_text="Your First Name", max_length=50),
                ),
                (
                    "last_name",
                    models.CharField(help_text="Your Last Name", max_length=50),
                ),
                ("email", models.EmailField(help_text="Your Email", max_length=100)),
            ],
            options={
                "verbose_name": "Subscriber",
                "verbose_name_plural": "Subscribers",
            },
        ),
    ]
