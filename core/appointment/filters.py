import jdatetime
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class JalaliDateRangeFilter(SimpleListFilter):
    title = _('Date Range')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return [
            ('tomorrow', _('Tomorrow')),
            ('this_week', _('This Week')),
            ('this_month', _('This Month')),
            ('next_week', _('Next Week')),
            ('next_month', _('Next Month')),
            ('this_year', _('This Year')),
        ]

    def queryset(self, request, queryset):
        today = jdatetime.date.today()

        # tomorrow
        if self.value() == 'tomorrow':
            tomorrow = today + jdatetime.timedelta(days=1)
            start_of_tomorrow = jdatetime.datetime.combine(tomorrow, jdatetime.time(0, 0))  # Start of day
            end_of_tomorrow = jdatetime.datetime.combine(tomorrow, jdatetime.time(23, 59, 59))  # End of day
            return queryset.filter(appointment_date__range=[start_of_tomorrow.togregorian(), end_of_tomorrow.togregorian()])

        # This Week
        if self.value() == 'this_week':
            start_of_week = today - jdatetime.timedelta(days=today.weekday())
            end_of_week = start_of_week + jdatetime.timedelta(days=6)
            return queryset.filter(appointment_date__range=[start_of_week.togregorian(), end_of_week.togregorian()])

        # This Month
        if self.value() == 'this_month':
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month + jdatetime.timedelta(days=30)  # End of the month calculation
            end_of_month = end_of_month.replace(day=1) - jdatetime.timedelta(days=1)
            return queryset.filter(appointment_date__range=[start_of_month.togregorian(), end_of_month.togregorian()])

        # Next Week
        if self.value() == 'next_week':
            start_of_next_week = today + jdatetime.timedelta(days=(7 - today.weekday()))
            end_of_next_week = start_of_next_week + jdatetime.timedelta(days=6)
            return queryset.filter(
                appointment_date__range=[start_of_next_week.togregorian(), end_of_next_week.togregorian()])

        # Next Month
        if self.value() == 'next_month':
            if today.month == 12:
                # If current month is Esfand (month 12), the next month will be Farvardin (month 1 of the next year)
                start_of_next_month = today.replace(year=today.year + 1, month=1, day=1)
            else:
                # Otherwise, just increment the month
                start_of_next_month = today.replace(month=today.month + 1, day=1)

            # Calculate the end of the next month
            if start_of_next_month.month == 12:
                end_of_next_month = start_of_next_month.replace(day=29 if start_of_next_month.isleap() else 30)
            else:
                end_of_next_month = (start_of_next_month + jdatetime.timedelta(days=31)).replace(
                    day=1) - jdatetime.timedelta(days=1)

            return queryset.filter(
                appointment_date__range=[start_of_next_month.togregorian(), end_of_next_month.togregorian()])
            # This Year
        if self.value() == 'this_year':
            start_of_year = today.replace(month=1, day=1)  # First day of the current Jalali year
            end_of_year = today.replace(month=12,
                                        day=30 if today.isleap() else 29)  # Last day of the current Jalali year
            return queryset.filter(appointment_date__range=[start_of_year.togregorian(), end_of_year.togregorian()])

        return queryset
