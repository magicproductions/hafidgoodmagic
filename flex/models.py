from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.panels import MultiFieldPanel, InlinePanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.models import Orderable

from streams import blocks


# class FlexCarousel(Orderable):
#     page = ParentalKey('flex.FlexPage', related_name='flex_carousel')
#     carousel_image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#
#     carousel_video = models.ForeignKey(
#         'wagtailvideos.Video',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#
#     panels = [
#         FieldPanel('carousel_image'),
#         FieldPanel('carousel_video'),
#     ]


class FlexPage(Page):
    """Flexible page class"""
    template = 'flex/flex_page.html'
    subpage_types = [
        'flex.FlexPage',
        'contact.ContactPage',
    ]
    parent_page_types = [
        'flex.FlexPage',
        'home.HomePage',
    ]
    
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    content = StreamField(
        [
            ('flex_block', blocks.FlexPageBlock()),
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichtextBlock()),
            ('simple_richtext', blocks.SimpleRichtextBlock()),
            ('card_block', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
            ('simple_btn', blocks.ButtonBlock()),
            ('flex_carousel', blocks.FlexCarousel()),
            ('gallery', blocks.GalleryBlock()),
        ],
        null=True,
        blank=True
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('hero_image'),
        FieldPanel('content'),
    ]
    
    class Meta:
        verbose_name = 'Flex Page'
        verbose_name_plural = 'Flex Pages'
