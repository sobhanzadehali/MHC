from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .forms import PayDebtsForm
from .models import Debts,AppointmentCost
from .forms import PayDebtsForm


# Register your models here.


@admin.register(Debts)
class DebtsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Debts', {
            'fields': [
                'patient', 'amount','canceled'
            ],
        }),
    ]
    search_fields = ['patient__name', 'patient__student_number']
    list_display = ['patient', 'amount']
    list_filter = ['patient']
    readonly_fields = ['amount', 'canceled']
    actions = ['pay_debt']

    def get_urls(self):
        # Add custom URL to the admin
        urls = super().get_urls()  # This ensures the default URLs are included
        custom_urls = [
            path('pay-debt/', self.pay_debt_view, name='pay_debt'),  # Define the custom URL
        ]
        return custom_urls + urls  # Add custom URLs at the beginning or end of the default ones

    def pay_debt_view(self, request):
        # Handle the custom view for paying debts
        if request.method == 'POST':
            form = PayDebtsForm(request.POST)
            if form.is_valid():
                debt = form.save(commit=False)
                debt.pay_debt()  # Call your custom logic to pay the debt
                self.message_user(request, "Debt successfully paid.")
                return redirect('admin:app_userdebt_changelist')  # Redirect to the list view
        else:
            form = PayDebtsForm()

        return render(request, 'admin/pay_debt.html', {'form': form})

    def pay_debt(self, request, queryset):
        # A custom admin action to mark debts as paid
        for debt in queryset:
            debt.pay_debt()
        self.message_user(request, "Selected debts have been paid.")
    pay_debt.short_description = _("Pay selected debts")

admin.site.register(AppointmentCost)