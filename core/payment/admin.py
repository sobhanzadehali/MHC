from django.contrib import admin
from .models import Debts

# Register your models here.


@admin.register(Debts)
class DebtsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Debts', {
            'fields': [
                'patient','amount'
            ],
        }),
    ]
    search_fields = ['patient__name','patient__student_number']
    list_display = ['patient','amount']
    list_filter = ['patient']
    readonly_fields = ['amount']