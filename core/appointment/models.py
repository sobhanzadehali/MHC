from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(_('name'),max_length=255)
    specialization = models.CharField(_('specialization'), max_length=255, help_text=_('doctor specialization'))
    phone_number = models.CharField(_('phone'), max_length=11)
    
    def __str__(self) -> str:
        return self.name
    
    