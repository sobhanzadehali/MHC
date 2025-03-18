from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class AppointmentCost(models.Model):
    appointment_type = models.CharField(max_length=255, verbose_name=_('appointment type'))
    cost = models.BigIntegerField(verbose_name=_('cost'))

    class Meta:
        verbose_name = _('appointment cost')
        verbose_name_plural = _('appointment costs')
