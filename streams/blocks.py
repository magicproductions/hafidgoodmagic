from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.core import blocks
from wagtail.core.templatetags.wagtailcore_tags import richtext
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtailvideos.blocks import VideoChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""
    
    title = blocks.CharBlock(required=True, help_text=_("Add your title"))
    text = blocks.TextBlock(required=True, help_text=_("Add additional text"))
    
    class Meta:  # noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class BlockQuote(blocks.StructBlock):
    text = blocks.TextBlock(required=False)
    quote_author = blocks.CharBlock(required=False)
    
    class Meta:  # noqa
        template = 'streams/blockquote.html'
        icon = 'quote'
        label = 'Quote'


class CardBlock(blocks.StructBlock):
    """Cards with image and text and button."""
    
    title = blocks.CharBlock(required=True, help_text=_("Add your title"))
    
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                (
                    "button_url",
                    blocks.URLBlock(
                        required=False,
                        help_text=_("If the button page above is selected, that will be used first."),  # noqa
                    ),
                ),
            ]
        )
    )
    
    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Cards Block"


class ProjectsBlock(blocks.StructBlock):
    """Block for Home Page Projects"""
    
    title = blocks.CharBlock(required=True, max_length=60, help_text=_("Add your title"))
    
    project_info = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('title', blocks.CharBlock(required=True, max_length=60)),
                ('image', ImageChooserBlock(required=True)),
                (
                    'button_url',
                    blocks.URLBlock(
                        required=False,
                        help_text=_("URL to go to.")  # noqa
                    ),
                ),
                # ('open_in_new_tab', blocks.BooleanBlock(required=False, default=False, blank=True))
            ]
        )
    )
    
    # @property
    # def link(self):
    #     if self.project_info.button_page:
    #         return self.project_info.button_page
    #     elif self.project_info.button_url:
    #         return self.project_info.button_url
    #     return '#'
    
    class Meta:  # noqa
        template = 'streams/project_block.html'
        icon = 'form'
        label = _('Projects Block')


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""
    
    def get_api_representation(self, value, context=None):
        return richtext(value.source)
    
    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichtextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""
    
    def __init__(
            self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]
    
    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"


class CTABlock(blocks.StructBlock):
    """A simple call to action section."""
    
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(
        required=True,
        default=_('Learn More'),
        max_length=40
    )
    
    cta_bg_image = ImageChooserBlock(required=True)
    
    class Meta:  # noqa
        template = 'streams/cta_block.html'
        icon = 'pick'
        label = _('Call to Action')


class HomeMainBlock(blocks.StructBlock):
    """A simple call to action section."""
    
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(
        required=True,
        default=_('Learn More'),
        max_length=40
    )
    
    block_image = ImageChooserBlock(required=False)
    
    block_video = VideoChooserBlock(required=False)
    
    class Meta:  # noqa
        template = 'streams/main_block.html'
        icon = 'pick'
        label = _('Main Block')


class HomeServicesBlock(blocks.StructBlock):
    """A simple Services Block section."""
    
    section_title = blocks.CharBlock(required=True, max_length=60)
    text_intro = blocks.TextBlock(required=False, max_length=500)
    
    service_info = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('title', blocks.CharBlock(required=True, max_length=60)),
                ('text', blocks.RichTextBlock(required=True, features=["bold", "italic"])),
                ('button_page', blocks.PageChooserBlock(required=False)),
                ('button_text', blocks.CharBlock(required=True, default=_('Learn More'), max_length=40))
            ]
        )
    )
    
    class Meta:  # noqa
        template = 'streams/services_block.html'
        icon = 'pick'
        label = _('Services Block')


class TestimonialBlock(blocks.StructBlock):
    """A simple Services Block section."""
    
    bg_image = ImageChooserBlock(required=False)
    testimonials = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('text', blocks.RichTextBlock(required=True, features=["bold", "italic"])),
                ('author', blocks.CharBlock(required=True, max_length=60)),
            ]
        )
    )
    
    class Meta:  # noqa
        template = 'streams/testimonial_block.html'
        icon = 'pick'
        label = _('Testimonials')


class BrandsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    grey_title = blocks.CharBlock(required=False)
    
    brands_images = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=False))
            ]
        )
    )
    
    class Meta:
        template = 'streams/brands_block.html'
        icon = 'pick'
        label = _('Brands Image & Logo')


class FlexPageBlock(blocks.StructBlock):
    """Template for Flex Pages"""
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True)
    
    class Meta:
        template = 'streams/flex_block.html'
        icon = 'pick'
        label = _('Flex Block Content')


class FlexCarousel(blocks.StructBlock):
    """Flex Pages Carousel"""
    
    items_carousel = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=False)),
                ('video', VideoChooserBlock(required=False)),
                ('video_poster', ImageChooserBlock(required=False)),
            ]
        )
    )
    
    class Meta:
        template = 'streams/flex_carousel.html'
        icon = 'pick'
        label = _('Flex Block Carousel')


class GalleryBlock(blocks.StructBlock):
    """Gallery Block"""
    
    items_gallery = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=False)),
            ]
        )
    )
    
    class Meta:
        template = 'streams/gallery_block.html'
        icon = 'pick'
        label = _('Gallery')


class ScrollingTextBlock(blocks.StructBlock):
    """A simple Text Input"""
    
    text_1 = blocks.CharBlock(required=True, max_length=80, features=['bold', 'italic'])
    text_2 = blocks.CharBlock(required=True, max_length=80, features=['bold', 'italic'])
    
    class Meta:  # noqa
        template = 'streams/scrolling_text.html'
        icon = 'pick'
        label = _('Scrolling Text')


class LinkStructValue(blocks.StructValue):
    """Additional logic for urls button."""
    
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        
        return None


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""
    
    button_page = blocks.PageChooserBlock(
        required=False,
        help_text='If selected, this url will be used first'
    )
    button_url = blocks.URLBlock(
        required=False,
        help_text='If added, this url will be used secondarily to the button page'
    )
    
    class Meta:  # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue
