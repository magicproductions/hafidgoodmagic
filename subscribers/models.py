from django.db import models
from django.utils.translation import gettext_lazy as _


class Subscriber(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False, help_text=_('Your First Name'))
    last_name = models.CharField(max_length=50, blank=False, null=False, help_text=_('Your Last Name'))
    email = models.EmailField(max_length=100, blank=False, null=False, help_text=_('Your Email'))
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.full_name()
    
    class Meta:  # noqa
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')
