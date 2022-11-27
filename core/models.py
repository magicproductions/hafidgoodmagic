# from django.db import models
# from django_extensions.db.fields import AutoSlugField
# from django.utils.translation import gettext_lazy as _
#
# from wagtail.core.models import Page
# from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
# from wagtail.images.edit_handlers import ImageChooserPanel
# from wagtail.snippets.models import register_snippet
# from wagtail.core.fields import StreamField
#
# from wagtailsvg.models import Svg
# from wagtailsvg.blocks import SvgChooserBlock
# from wagtailsvg.edit_handlers import SvgChooserPanel
#
#
# @register_snippet
# class SiteLogo(Page):
#     # template = 'wagtailadmin/base.html'
#     name = models.CharField(
#         max_length=100,
#         null=True,
#         blank=False,
#         help_text=_('Site main logo')
#     )
#
#     logo_slug = AutoSlugField(populate_from="name", editable=True)
#
#     # noinspection PyUnresolvedReferences
#     site_logo_image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#
#     main_logo_svg = models.ForeignKey(
#         Svg,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+'
#     )
#     body = StreamField(
#         [
#             ('svg', SvgChooserBlock()),
#         ], blank=True
#     )
#
#     panels = [
#         MultiFieldPanel(
#             [
#                 FieldPanel('name'),
#                 FieldPanel('logo_slug'),
#                 ImageChooserPanel('site_logo_image'),
#                 SvgChooserPanel('main_logo_svg'),
#                 FieldPanel('body'),
#             ],
#             heading='Name and Image'
#         ),
#     ]
#
#     def __str__(self):
#         return self.name
