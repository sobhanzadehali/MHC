from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali
from django_jalali.db import models as jmodels

# Create your models here.

User = get_user_model()


class Specialty(models.Model):
    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        verbose_name = _('Specialty')
        verbose_name_plural = _('Specialties')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    specialization = models.ForeignKey('appointment.Specialty', on_delete=models.CASCADE)
    phone_number = models.CharField(_('phone'), max_length=11)
    objects = jmodels.jManager()

    class Meta:
        unique_together = (('name', 'phone_number'),)
        verbose_name = _('Doctor')
        verbose_name_plural = _('Doctors')

    def __str__(self) -> str:
        return self.name


class Patient(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    phone_number = models.CharField(_('phone'), max_length=11)
    file_number = models.CharField(_('file number'), max_length=255)
    student_number = models.CharField(_('student number'), max_length=255, blank=True, null=True)
    objects = jmodels.jManager()

    class Meta:
        unique_together = (('name', 'phone_number'),)
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')

    def __str__(self) -> str:
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey('appointment.Doctor', on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey('appointment.Patient', on_delete=models.CASCADE, related_name='appointments')
    appointment_date = jmodels.jDateTimeField(_('appointment date'))
    description = models.TextField(_('description'), blank=True, null=True)

    objects = jmodels.jManager()

    class Meta:
        unique_together = (('doctor', 'patient', 'appointment_date'),)
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')

    def __str__(self):
        return f'{self.patient} - {self.doctor} for {self.appointment_date}'
