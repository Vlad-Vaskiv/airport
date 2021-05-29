from django.contrib import admin
from .models import *


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    pass


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    pass


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    pass


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    pass


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
