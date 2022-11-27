from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from django.utils.translation import gettext_lazy as _
from .models import Subscriber


class SubscriberAdmin(ModelAdmin):
    model = Subscriber
    menu_label = _('Subscribers')
    menu_icon = 'wagtail-inverse'
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)


modeladmin_register(SubscriberAdmin)
