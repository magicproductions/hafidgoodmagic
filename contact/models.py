from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField
from wagtailcaptcha.models import WagtailCaptchaEmailForm

from modelcluster.fields import ParentalKey


class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')
    #     Add custom fields to the FormField class
    field_classname = models.CharField('Field classes', max_length=255, blank=True)
    placeholder = models.CharField('Placeholder', max_length=255, blank=True)
    
    panels = AbstractFormField.panels + [
        FieldPanel('field_classname'),
        FieldPanel('placeholder'),
    ]


class CustomFormBuilder(FormBuilder):
    def get_create_field_function(self, type):
        """
        Override the method to prepare a wrapped function that will call the original
        function (which returns a field) and update the widget's attrs with a custom
        value that can be used within the template when rendering each field.
        """
        
        create_field_function = super().get_create_field_function(type)
        
        def wrapped_create_field_function(field, options):
            created_field = create_field_function(field, options)
            created_field.widget.attrs.update(
                {
                    "class": field.field_classname
                },
            )
            
            return created_field
        
        return wrapped_create_field_function


class ContactPage(WagtailCaptchaEmailForm):
    template = 'contact/contact_page.html'
    subpage_types = []
    parent_page_types = [
        'home.HomePage',
        # 'flex.FlexPage',
    ]
    
    intro = RichTextField(blank=True)
    form_builder = CustomFormBuilder
    thank_you_text = RichTextField(blank=True)
    
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('from_address', classname='col6'),
                        FieldPanel('to_address', classname='col6')
                    ]
                ),
                FieldPanel('subject'),
            ], heading='Email Settings'
        ),
    ]
