from django.contrib import admin
from .models import *


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    search_fields = ['username', 'phone', 'passport_number']


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    search_fields = ['name',]


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    search_fields = ['code', ]
    # inlines = [ModelInline, ]


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    # inlines = [AddressInline, ]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_filter = ['status', ]
    search_fields = ['flight_no', ]
    date_hierarchy = 'scheduled_departure'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(FareConditionPrice)
class FareConditionPriceAdmin(admin.ModelAdmin):
    pass
