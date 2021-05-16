from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


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
    model = ModelSerializer(many=False)
    seats = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())

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


class FlightSerializer(serializers.HyperlinkedModelSerializer):
    departure_airport = AirportSerializer(many=False)
    arrival_airport = AirportSerializer(many=False)
    aircraft = AircraftSerializer(many=False)

    class Meta:
        model = Flight
        fields = "__all__"


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    aircraft = AircraftSerializer(many=False)

    class Meta:
        model = Seat
        fields = "__all__"


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=8, decimal_places=2, required=False
    )

    class Meta:
        model = Ticket
        fields = "__all__"
