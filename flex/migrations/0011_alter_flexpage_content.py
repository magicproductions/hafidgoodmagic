# Generated by Django 4.1.3 on 2022-11-26 21:50

from django.db import migrations
import streams.blocks
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailvideos.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("flex", "0010_alter_flexpage_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flexpage",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    (
                        "flex_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        max_length=60, required=True
                                    ),
                                ),
                                ("text", wagtail.blocks.RichTextBlock(required=True)),
                            ]
                        ),
                    ),
                    (
                        "title_and_text",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Add your title", required=True
                                    ),
                                ),
                                (
                                    "text",
                                    wagtail.blocks.TextBlock(
                                        help_text="Add additional text", required=True
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("full_richtext", streams.blocks.RichtextBlock()),
                    ("simple_richtext", streams.blocks.SimpleRichtextBlock()),
                    (
                        "card_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        help_text="Add your title", required=True
                                    ),
                                ),
                                (
                                    "cards",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=True
                                                    ),
                                                ),
                                                (
                                                    "title",
                                                    wagtail.blocks.CharBlock(
                                                        max_length=40, required=True
                                                    ),
                                                ),
                                                (
                                                    "text",
                                                    wagtail.blocks.TextBlock(
                                                        max_length=200, required=True
                                                    ),
                                                ),
                                                (
                                                    "button_page",
                                                    wagtail.blocks.PageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "button_url",
                                                    wagtail.blocks.URLBlock(
                                                        help_text="If the button page above is selected, that will be used first.",
                                                        required=False,
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "cta",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.CharBlock(
                                        max_length=60, required=True
                                    ),
                                ),
                                (
                                    "text",
                                    wagtail.blocks.RichTextBlock(
                                        features=["bold", "italic"], required=True
                                    ),
                                ),
                                (
                                    "button_page",
                                    wagtail.blocks.PageChooserBlock(required=False),
                                ),
                                ("button_url", wagtail.blocks.URLBlock(required=False)),
                                (
                                    "button_text",
                                    wagtail.blocks.CharBlock(
                                        default="Learn More",
                                        max_length=40,
                                        required=True,
                                    ),
                                ),
                                (
                                    "cta_bg_image",
                                    wagtail.images.blocks.ImageChooserBlock(
                                        required=True
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "simple_btn",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "button_page",
                                    wagtail.blocks.PageChooserBlock(
                                        help_text="If selected, this url will be used first",
                                        required=False,
                                    ),
                                ),
                                (
                                    "button_url",
                                    wagtail.blocks.URLBlock(
                                        help_text="If added, this url will be used secondarily to the button page",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "flex_carousel",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "items_carousel",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "video",
                                                    wagtailvideos.blocks.VideoChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "video_poster",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    ),
                    (
                        "gallery",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "items_carousel",
                                    wagtail.blocks.ListBlock(
                                        wagtail.blocks.StructBlock(
                                            [
                                                (
                                                    "image",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "video",
                                                    wagtailvideos.blocks.VideoChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                                (
                                                    "video_poster",
                                                    wagtail.images.blocks.ImageChooserBlock(
                                                        required=False
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                )
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=None,
            ),
        ),
    ]
