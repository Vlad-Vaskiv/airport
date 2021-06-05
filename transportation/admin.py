from django.contrib import admin
from django.contrib.admin import StackedInline

from .models import *


class TicketInline(StackedInline):
    model = Ticket
    extra = 0


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    search_fields = ['phone', 'passport_number']
    date_hierarchy = 'birthday'
    list_display = ['passport_number', 'birthday', 'phone']
    inlines = [TicketInline, ]


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
    list_display = ['id', 'flight', 'seat', 'total_amount']
    date_hierarchy = 'created_at'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['country', 'city', 'line', 'lat', 'lon']
    list_filter = ['country']


@admin.register(FareConditionPrice)
class FareConditionPriceAdmin(admin.ModelAdmin):
    list_display = ['fare_condition', 'coef']
