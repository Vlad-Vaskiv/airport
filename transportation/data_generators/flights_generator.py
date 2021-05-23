from transportation.models import *
from .code_generator import id_generator
import datetime
import random
from django.utils import timezone


def generate_flights():
    for _ in range(0, 50):
        flight_no = id_generator(size=6)
        now = timezone.now()
        future = now + datetime.timedelta(seconds=random.randint(0, 259200))
        arr_future = future + datetime.timedelta(seconds=random.randint(14400, 15400))
        departure_airport = Airport.objects.order_by('?').first()
        arrival_airport = Airport.objects.order_by('?').first()
        aircraft = Aircraft.objects.order_by('?').first()
        Flight.objects.create(flight_no=flight_no,
                              scheduled_departure=future,
                              scheduled_arrival=arr_future,
                              departure_airport=departure_airport,
                              arrival_airport=arrival_airport,
                              aircraft=aircraft)
