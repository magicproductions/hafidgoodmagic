# Generated by Django 4.1.3 on 2022-11-25 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0024_index_image_file_hash"),
        ("flex", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="flexpage",
            name="hero_image",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
    ]
