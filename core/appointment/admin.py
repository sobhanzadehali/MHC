import csv
from django.contrib import admin
from django.db import models
from django.http import HttpResponse

from .models import Patient, Doctor, Appointment
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date.widgets import AdminSplitJalaliDateTime, AdminJalaliDateWidget
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from django_jalali.db import models as jmodels
# Register your models here.


def export_to_csv(modeladmin, request, queryset):
    # Create the response object to send the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['ID', 'Doctor', 'Patient', 'Date', 'Description'])  # Customize this as per your model fields

    # Write data rows
    for obj in queryset:
        writer.writerow([obj.id, obj.doctor, obj.patient, obj.appointment_date, obj.description])  # Customize this as per your model fields

    return response

export_to_csv.short_description = "Export selected to CSV"


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'specialization', 'phone_number')
    list_display = ('name', 'specialization', 'phone_number')



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'phone_number', 'student_number', 'file_number')
    list_display = ('name', 'phone_number', 'student_number', 'file_number')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_filter = (
        ('appointment_date', JDateFieldListFilter),
        'doctor__name',
    )
    autocomplete_fields = ['patient', 'doctor']
    list_display = ['patient', 'doctor', 'appointment_date']
    search_fields = ['patient__name', 'doctor__name']
    formfield_overrides = {
        jmodels.jDateField: {'widget': AdminJalaliDateWidget},
        jmodels.jDateTimeField: {'widget': AdminSplitJalaliDateTime},
    }
    actions = [export_to_csv]
