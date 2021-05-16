from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel


class FareConditions(models.TextChoices):
    economy = 'economy', "Economy"
    comfort = "comfort", "Comfort"
    business = "business", "Business"


class Passenger(models.Model):
    """Extending the existing User model for passenger representation"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passport_number = models.CharField(max_length=20)
    birthday = models.DateField()
    phone = models.CharField(max_length=15)
    email_confirmed = models.BooleanField(default=False)


class Model(BaseModel):
    """Class describing Aircraft model"""

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='models', null=True, blank=True)

    def __str__(self):
        return self.name


class Aircraft(BaseModel):
    """Aircraft representation"""

    code = models.CharField(max_length=3, unique=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    range = models.PositiveIntegerField(help_text='Maximum flight range, km')

    def __str__(self):
        return f'{self.code} - {self.model}'


class Address(BaseModel):
    """Address representation"""

    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    timezone = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f'{self.country} - {self.city}\n{self.line}'


class Airport(BaseModel):
    """Airport representation"""

    name = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)


class Flight(BaseModel):
    """Flight representation"""
    class Status(models.TextChoices):
        """Status enum"""
        scheduled = 'scheduled', 'Scheduled'
        on_time = 'on_time', 'On Time'
        delayed = 'delayed', 'Delayed'
        departed = 'departed', 'Departed'
        arrived = 'arrived', 'Arrived'
        cancelled = 'cancelled', 'Cancelled'

    flight_no = models.CharField(max_length=6)
    scheduled_departure = models.DateTimeField()
    scheduled_arrival = models.DateTimeField()
    departure_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='dep_flights')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name='arr_flights')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.scheduled)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT)
    actual_departure = models.DateTimeField(null=True, blank=True)
    actual_arrival = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (('flight_no', 'scheduled_departure'), )
        constraints = [
            models.CheckConstraint(check=models.Q(scheduled_arrival__gte=models.F('scheduled_departure')), name='greater_check'),
        ]


class Seat(BaseModel):
    """Seat representation"""

    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT, related_name='seats')
    seat_no = models.IntegerField()
    fare_condition = models.CharField(max_length=10, choices=FareConditions.choices)

    class Meta:
        unique_together = (('aircraft_id', 'seat_no'), )

    def __str__(self):
        return f'{self.aircraft_id} - {self.seat_no}'


class Ticket(BaseModel):
    """Ticket Booking representation"""

    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.passenger} - {self.flight} - {self.seat} - {self.total_amount}'


class FareConditionPrice(BaseModel):
    fare_condition = models.CharField(max_length=10, choices=FareConditions.choices)
    coef = models.DecimalField(max_digits=2, decimal_places=2, validators=[MinValueValidator(0.0)])


