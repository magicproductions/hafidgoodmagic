from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class SocialMediaSettings(BaseSetting):
    """Social Media Site Settings"""
    
    linkedin = models.URLField(blank=True, null=True, help_text=_('LinkedIn link.'))
    instagram = models.URLField(blank=True, null=True, help_text=_('Instagram link.'))
    facebook = models.URLField(blank=True, null=True, help_text=_('FaceBook link.'))
    twitter = models.URLField(blank=True, null=True, help_text=_('Twitter link.'))
    youtube = models.URLField(blank=True, null=True, help_text=_('YouTube link.'))
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('linkedin'),
                FieldPanel('instagram'),
                FieldPanel('facebook'),
                FieldPanel('twitter'),
                FieldPanel('youtube'),
            ], heading=_('Social Media Settings')
        )
    ]
