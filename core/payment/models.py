from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from appointment.models import Patient, Appointment
from django.utils.translation import gettext_lazy as _


# Create your models here.

class AppointmentCost(models.Model):
    price = models.BigIntegerField(_("price"), default=0)

    class Meta:
        verbose_name = _("Appointment Cost")
        verbose_name_plural = _("Appointment Costs")

    def save(self, *args, **kwargs):
        if not self.pk and AppointmentCost.objects.exists():
            raise ValidationError("only one appointment cost is allowed")
        super(AppointmentCost, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.price)


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
        user_appointments = Appointment.objects.filter(patient=self.patient, is_paid=False).count()
        try:
            cost = AppointmentCost.objects.all()[0].price
            amount += cost * user_appointments
        except AppointmentCost.DoesNotExist:
            raise ValidationError(_("no appointment cost, set a cost in appointment cost model"))

        return amount

    @property
    def canceled(self):
        count = 0
        count = Appointment.objects.filter(patient=self.patient, is_canceled=True).count()
        return count

    def pay_debt(self):
        user_appointments = Appointment.objects.filter(patient=self.patient, is_paid=False)
        for appointment in user_appointments:
            appointment.is_paid = True
            appointment.save()


@receiver(post_save, sender=Patient)
def create_patient_debt(sender, instance, created, **kwargs):
    if created:
        Debts.objects.create(patient=instance)
