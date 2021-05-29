from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from .utils import calculate_total_amount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]


class SignupSerializer(serializers.ModelSerializer):
    """Signup serializer"""

    user = UserSerializer(many=False, required=True)

    class Meta:
        model = Passenger
        exclude = [
            "email_confirmed",
        ]


class PassengerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"


class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"


class AircraftSerializer(serializers.HyperlinkedModelSerializer):
    model = ModelSerializer(many=False, read_only=True)
    # seats = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())

    class Meta:
        model = Aircraft
        fields = "__all__"


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class AirportSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer(many=False)

    class Meta:
        model = Airport
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    departure_airport = AirportSerializer(many=False, read_only=True)
    arrival_airport = AirportSerializer(many=False, read_only=True)
    aircraft = AircraftSerializer(many=False, read_only=True)

    class Meta:
        model = Flight
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=8, decimal_places=2, required=False
    )
    # passenger = PassengerSerializer(many=False)

    class Meta:
        model = Ticket
        # fields = "__all__"
        fields = ["flight_id", 'seat_id', 'total_amount']


class SeatSerializer(serializers.ModelSerializer):
    aircraft = AircraftSerializer(many=False, read_only=True)
    ticket = TicketSerializer(source='ticket_set', read_only=True)
    price = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = "__all__"

    def get_price(self, seat):
        flight = Flight.objects.get(id=seat.flight_id)
        return calculate_total_amount(flight, seat)
