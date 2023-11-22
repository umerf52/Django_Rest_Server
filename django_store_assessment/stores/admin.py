from django.contrib import admin

from django_store_assessment.stores.models import Store, OpeningHours, Address


# Register your models here.


class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('weekday', 'from_hour', 'to_hour')
    list_filter = ('weekday',)
    ordering = ('weekday', 'from_hour')
    search_fields = ('weekday',)


admin.site.register(OpeningHours, OpeningHoursAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'state', 'postal_code', 'country')
    list_filter = ('country',)
    ordering = ('country', 'state', 'city', 'street')
    search_fields = ('street', 'city', 'state', 'postal_code', 'country')


admin.site.register(Address, AddressAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'days_open')

    def days_open(self, obj):
        # Calculate the number of unique days the store is open
        unique_days = obj.opening_hours.values_list('weekday', flat=True).distinct()
        return len(unique_days)

    days_open.short_description = 'Days Open Per Week'


admin.site.register(Store, StoreAdmin)
