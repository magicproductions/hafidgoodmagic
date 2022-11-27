from django.db import models
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from wagtail.api import APIField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel,
)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
# from wagtail.images.blocks import ImageChooserBlock
# from wagtail.images.edit_handlers import ImageChooserPanel
# from wagtail.snippets.models import register_snippet
# from wagtail.snippets.edit_handlers import SnippetChooserPanel
# from django_extensions.db.fields import AutoSlugField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

# from wagtailcaptcha.models import WagtailCaptchaEmailForm

from streams import blocks


# class HomePageCarouselImages(Orderable):
#     page = ParentalKey('home.HomePage', related_name='home_banner_carousel')
#     # noinspection PyUnresolvedReferences
#     carousel_image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=False,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#
#     heading = models.CharField(
#         max_length=140,
#         blank=True,
#         null=True,
#         help_text='Heading text'
#     )
#     lead_text = models.CharField(
#         max_length=140,
#         blank=True,
#         help_text='Subheading text'
#     )
#     short_description = models.CharField(
#         max_length=150,
#         blank=True,
#         null=True,
#         help_text='Short description'
#     )
#     # noinspection PyUnresolvedReferences
#     button = models.ForeignKey(
#         'wagtailcore.Page',
#         blank=True,
#         null=True,
#         related_name='+',
#         help_text='Select a page to link to',
#         on_delete=models.SET_NULL,
#     )
#     button_text = models.CharField(
#         max_length=50,
#         default='Read More',
#         blank=False,
#         help_text='Button text',
#     )
#
#     panels = [
#         FieldPanel('heading'),
#         FieldPanel('lead_text'),
#         FieldPanel('short_description'),
#         PageChooserPanel('button'),
#         FieldPanel('button_text'),
#         FieldPanel('carousel_image'),
#     ]
#
#     api_fields = [
#         APIField('heading'),
#         APIField('lead_text'),
#         APIField('short_description'),
#         APIField('button'),
#         APIField('button_text'),
#         APIField('carousel_image'),
#     ]


# class HomePageServices(Orderable):
#     page = ParentalKey('home.HomePage', related_name='services')
#     title = models.CharField(
#         max_length=60,
#         blank=False,
#         null=True,
#         help_text='Section Title'
#     )
#     description = models.CharField(
#         max_length=500,
#         blank=True,
#         null=True,
#         help_text='Section Description'
#     )
#
#     panels = [
#         FieldPanel('title'),
#         FieldPanel('description'),
#     ]


class HomeHero(Orderable):
    page = ParentalKey('home.HomePage', related_name='home_hero')
    main_title = models.CharField(
        blank=False,
        null=True,
        max_length=12,
        help_text='Home Hero Main Title.',
    )
    # noinspection PyUnresolvedReferences
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    text_line1 = models.CharField(
        max_length=20,
        blank=False,
        null=True,
        help_text='Text Line 1'
    )
    text_line2 = models.CharField(
        max_length=26,
        blank=False,
        null=True,
        help_text='Text Line 2'
    )
    text_line3 = models.CharField(
        max_length=26,
        blank=False,
        null=True,
        help_text='Text Line 3'
    )
    text_line4 = models.CharField(
        max_length=26,
        blank=False,
        null=True,
        help_text='Text Line 4'
    )
    
    panels = [
        FieldPanel('main_title'),
        FieldPanel('hero_image'),
        FieldPanel('text_line1'),
        FieldPanel('text_line2'),
        FieldPanel('text_line3'),
        FieldPanel('text_line4'),
    ]


# class FormField(AbstractFormField):
#     page = ParentalKey('HomePage', related_name='custom_form_fields')


class HomePage(RoutablePageMixin, Page):
    """Home Page Model"""
    
    template = 'home/home_page.html'
    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ]
    
    parent_page_types = ['wagtailcore.Page']
    # max_count = 1
    
    # description = models.CharField(max_length=255, blank=True, )
    # thank_you_text = RichTextField(blank=True)
    
    main_blocks = StreamField(
        [
            ('main_blocks', blocks.HomeMainBlock()),
        ],
        blank=True,
        null=True,
    )
    
    content = StreamField(
        [
            ('cta', blocks.CTABlock()),
            ('project_block', blocks.ProjectsBlock()),
            ('home_services', blocks.HomeServicesBlock()),
            ('testimonials', blocks.TestimonialBlock()),
            ('scrolling_text', blocks.ScrollingTextBlock()),
            ('brands_images', blocks.BrandsBlock()),
        ],
        null=True,
        blank=True
    )
    
    api_fields = [
        # APIField('main_logo'),
        # APIField('main_title'),
        APIField('content'),
        APIField('home_banner_carousel'),
    ]
    
    content_panels = Page.content_panels + AbstractEmailForm.content_panels + [
        InlinePanel('home_hero', label='Main Home Hero', max_num=1),
        FieldPanel('main_blocks'),
        FieldPanel('content'),
        
        # MultiFieldPanel(
        #     [
        #         InlinePanel('home_banner_carousel', max_num=5, min_num=1, label=_(' Carousel Block')),
        #     ],
        #     heading=_('Main Carousel Banner'),
        #     classname="collapsible collapsed",
        # ),
        # MultiFieldPanel(
        #     [
        #         InlinePanel('services', max_num=6, min_num=1, label=_(' Services'))
        #     ],
        #     heading=_('Our Services'),
        #     classname="collapsible collapsed",
        # ),
        
        # FieldPanel('description', classname="full"),
        # InlinePanel('custom_form_fields', label="Form fields"),
        # FieldPanel('thank_you_text', classname="full"),
        # MultiFieldPanel(
        #     [
        #         FieldRowPanel(
        #             [
        #                 FieldPanel('from_address', classname="col6"),
        #                 FieldPanel('to_address', classname="col6"),
        #             ]
        #         ),
        #         FieldPanel('subject'),
        #     ], "Email Notification Config"
        # ),
    ]
    
    # def get_form_fields(self):
    #     return self.custom_form_fields.all()
    
    class Meta:
        verbose_name = _('Home Page')
        verbose_name_plural = _('Home pages')
    
    @route(r'^subscribe/$')
    def subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, 'home/subscribe.html', context)

# HomePage._meta.get_field('title').verbose_name = 'New Title'
# HomePage._meta.get_field('title').help_text = 'the help text will be HERE!!!'
