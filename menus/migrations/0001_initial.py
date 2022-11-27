# Generated by Django 4.1.3 on 2022-11-25 01:41

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0078_referenceindex"),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
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
                ("title", models.CharField(max_length=100)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from="title"
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="MenuItem",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("link_title", models.CharField(blank=True, max_length=50, null=True)),
                ("number", models.CharField(max_length=1, null=True)),
                ("link_url", models.CharField(blank=True, max_length=500)),
                ("open_in_new_tab", models.BooleanField(blank=True, default=False)),
                (
                    "link_page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="wagtailcore.page",
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu_items",
                        to="menus.menu",
                    ),
                ),
            ],
            options={"ordering": ["sort_order"], "abstract": False,},
        ),
    ]
