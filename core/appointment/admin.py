import csv
from django.contrib import admin
from django.http import HttpResponse
import jdatetime
from .models import Patient, Doctor, Appointment, Specialty
from .filters import JalaliDateRangeFilter
from jalali_date.widgets import AdminSplitJalaliDateTime, AdminJalaliDateWidget
# from django_jalali.admin.filters import JDateFieldListFilter
from django_jalali.db import models as jmodels


# Register your models here.


def export_appointments_to_csv(modeladmin, request, queryset):
    # Create the response object to send the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['ID', 'Doctor', 'Patient', 'Date', 'Description'])  # Customize this as per your model fields

    # Write data rows
    for obj in queryset:
        writer.writerow([obj.id, obj.doctor, obj.patient, obj.appointment_date,
                         obj.description])  # Customize this as per your model fields

    return response


export_appointments_to_csv.short_description = "Export selected to CSV"


def export_patients_to_csv(modeladmin, request, queryset):
    # Create the response object to send the CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(
        ['ID', 'Name', 'Phone Number', 'File Number', 'Student Number'])  # Customize this as per your model fields

    # Write data rows
    for obj in queryset:
        writer.writerow([obj.id, obj.name, obj.phone_number, obj.file_number,
                         obj.student_number])  # Customize this as per your model fields

    return response


export_patients_to_csv.short_description = "Export selected to CSV"


@admin.register(Specialty)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    autocomplete_fields = ['specialization', ]
    search_fields = ('name', 'specialization__name', 'phone_number')
    list_display = ('name', 'specialization', 'phone_number')
    list_filter = ('specialization',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ('name', 'phone_number', 'student_number', 'file_number')
    list_display = ('name', 'phone_number', 'student_number', 'file_number')
    actions = [export_patients_to_csv,]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_filter = (
        # ('appointment_date', JDateFieldListFilter),
        JalaliDateRangeFilter,
        'doctor__name',
    )
    autocomplete_fields = ['patient', 'doctor']
    list_display = ['patient', 'doctor', 'appointment_date']
    search_fields = ['patient__name', 'doctor__name', 'patient__file_number', 'patient__phone_number',
                     'patient__student_number', 'appointment_date']
    fieldsets = [
        ('appointment', {
            'fields': [
                'patient','doctor','appointment_date','description','is_paid',
            ],
        }),
    ]
    formfield_overrides = {
        jmodels.jDateField: {'widget': AdminJalaliDateWidget},
        jmodels.jDateTimeField: {'widget': AdminSplitJalaliDateTime},
    }
    actions = [export_appointments_to_csv]

    def get_search_results(self, request, queryset, search_term):
        # Call the default search behavior
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        try:
            # Try to parse the search term as a Jalali date in 'YYYY-MM-DD' format
            search_date_jalali = jdatetime.datetime.strptime(search_term, '%Y-%m-%d').date()

            # Filter by date, ignoring time
            queryset |= self.model.objects.filter(
                appointment_date__date=search_date_jalali
            )
        except ValueError:
            # If search_term is not a valid Jalali date, skip filtering by date
            pass

        return queryset, use_distinct
