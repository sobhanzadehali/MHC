from django.conf import settings
from django.db import models
from appointment.models import Patient, Appointment
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Debts(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name=_('patient'))

    class Meta:
        verbose_name = _('debts')
        verbose_name_plural = _('debts')

    def __str__(self):
        return self.patient.name
    @property
    def amount(self):
        amount = 0
        user_appointments = Appointment.objects.filter(patient=self.patient, is_paid=False)
        for appointment in user_appointments:
            amount += settings.THERAPY_COST

        return amount

