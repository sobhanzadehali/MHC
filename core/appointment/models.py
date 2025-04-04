from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from jalali_date import datetime2jalali
from django_jalali.db import models as jmodels

# Create your models here.

User = get_user_model()


class Specialty(models.Model):
    """
    Represents a medical specialty or field of expertise for doctors.

    This model stores different medical specialties that doctors can be associated with,
    such as cardiology, pediatrics, etc.

    Attributes:
        name (str): The name of the medical specialty (max length: 255 characters)
    """
    name = models.CharField(_('Name'), max_length=255)

    class Meta:
        verbose_name = _('Specialty')
        verbose_name_plural = _('Specialties')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """
    Represents a medical doctor in the system.

    This model stores information about doctors including their personal details
    and their medical specialty.

    Attributes:
        name (str): The full name of the doctor (max length: 255 characters)
        specialization (Specialty): Foreign key to the doctor's medical specialty
        phone_number (str): Doctor's contact phone number (max length: 11 characters)

    Note:
        - Uses jManager for Jalali (Persian) date support
        - Enforces unique constraint on combination of name and phone number
    """
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
    """
    Represents a patient in the medical system.

    This model stores information about patients including their personal details
    and identification numbers.

    Attributes:
        name (str): The full name of the patient (max length: 255 characters)
        phone_number (str): Patient's contact phone number (max length: 11 characters)
        file_number (str, optional): Patient's medical file number
        student_number (str, optional): Student identification number if applicable

    Note:
        - Uses jManager for Jalali (Persian) date support
        - Enforces unique constraint on combination of name and phone number
    """
    name = models.CharField(_("Name"), max_length=255)
    phone_number = models.CharField(_('phone'), max_length=11)
    file_number = models.CharField(_('file number'), max_length=255, blank=True, null=True)
    student_number = models.CharField(_('student number'), max_length=255, blank=True, null=True)
    objects = jmodels.jManager()

    class Meta:
        unique_together = (('name', 'phone_number'),)
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')

    def __str__(self) -> str:
        return self.name


class Appointment(models.Model):
    """
    Represents a medical appointment between a doctor and a patient.

    This model manages the scheduling of appointments, including the date, status,
    and any additional information about the appointment.

    Attributes:
        doctor (Doctor): Foreign key to the doctor conducting the appointment
        patient (Patient): Foreign key to the patient attending the appointment
        appointment_date (jDateTimeField): Date and time of the appointment in Jalali calendar
        description (str, optional): Additional notes or description about the appointment
        is_paid (bool): Payment status of the appointment, defaults to False
        is_canceled (bool): Cancellation status of the appointment, defaults to False

    Note:
        - Uses jManager for Jalali (Persian) date support
        - Enforces unique constraint on combination of doctor, patient, and appointment date
        - Provides method to cancel appointments

    Methods:
        cancel_appointment(): Marks the appointment as canceled
    """
    doctor = models.ForeignKey('appointment.Doctor', on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey('appointment.Patient', on_delete=models.CASCADE, related_name='appointments')
    appointment_date = jmodels.jDateTimeField(_('appointment date'))
    description = models.TextField(_('description'), blank=True, null=True)
    is_paid = models.BooleanField(_('is paid'), default=False)
    is_canceled = models.BooleanField(_('is canceled'), default=False)

    objects = jmodels.jManager()

    class Meta:
        unique_together = (('doctor', 'patient', 'appointment_date'),)
        verbose_name = _('Appointment')
        verbose_name_plural = _('Appointments')

    def __str__(self):
        return f'{self.patient} - {self.doctor} for {self.appointment_date}'

    def cancel_appointment(self):
        """
        Cancels the appointment by setting is_canceled to True and saving the instance.
        """
        self.is_canceled = True
        self.save()

