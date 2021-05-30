import coreapi
import coreschema
from django.db.models import Prefetch, Value, CharField, IntegerField
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django_filters import rest_framework as filters
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db import models
from rest_framework.schemas import ManualSchema, AutoSchema
from rest_framework.views import APIView
from .utils import calculate_total_amount
import datetime
from .models import *
from .serializers import *

from base.tokens import account_activation_token


class AirportView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class PassengerView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ("user__email",)


class ModelView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class AircraftView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer


class AddressView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class FlightView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        departure_airport__address__city = self.request.query_params.get("departure_airport__address__city")
        arrival_airport__address__city = self.request.query_params.get('arrival_airport__address__city')
        scheduled_departure = self.request.query_params.get('scheduled_departure')
        queryset = super().get_queryset()
        if departure_airport__address__city:
            queryset = queryset.filter(departure_airport__address__city=departure_airport__address__city)
        if arrival_airport__address__city:
            queryset = queryset.filter(arrival_airport__address__city=arrival_airport__address__city)
        if scheduled_departure:
            queryset = queryset.filter(scheduled_departure__date=datetime.datetime.strptime(scheduled_departure,
                                                                                            "%d-%m-%Y")
                                       .date())

        return queryset


class SeatView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_queryset(self):
        flight_id = self.request.query_params.get("flight_id")
        flight = Flight.objects.filter(id=flight_id).first()
        if not flight_id or not flight:
            raise ValidationError(detail='aircraft_id is missed or flight does not exist!')
        queryset = super().get_queryset()
        return queryset.filter(aircraft_id=flight.aircraft_id).prefetch_related(
            Prefetch('ticket_set', queryset=Ticket.objects.filter(flight=flight), to_attr='ticket_obj'
                     ),
        ).annotate(flight_id=Value(flight_id, output_field=IntegerField()))


class TicketView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()
    serializer_class = CreateTicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Account.objects.create_user(**serializer.validated_data)
            Ticket.objects.create(passenger=Passenger.objects.get(user=request.user), **serializer.validated_data)
            return Response({'message': 'Ticket created'}, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Ticket could not be created with received data'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return self.queryset.filter(passenger=Passenger.objects.get(self.request.user))


class PriceView(APIView):
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "flight_id",
                required=True,
                location="path",
                schema=coreschema.Integer(
                    title="Flight ID",
                    description="Flight ID.",
                ),
            ),
            coreapi.Field(
                "seat_id",
                location="query",
                required=True,
                schema=coreschema.Integer(
                    title="Seat ID",
                    description="Seat ID",
                ),
            ),
        ],
    )

    def get(self, request, format=None):
        flight_id = request.query_params.get("flight_id")
        seat_id = request.query_params.get("seat_id")
        if flight_id and seat_id:
            flight = Flight.objects.get(id=flight_id)
            seat = Seat.objects.get(id=seat_id)
            total_amount = calculate_total_amount(flight, seat)
            return Response({"total_amount": total_amount})
        return Response(status=400)


class Signup(generics.CreateAPIView):
    """
    Register User
    """

    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        raw_user = request.data.pop("user")
        if User.objects.filter(
            models.Q(email=raw_user.get("email"))
        ).exists():
            return Response(
                data={
                    "message": f"User with email {raw_user.get('email')} already exist"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # user = User.objects.create_user(is_active=False, **raw_user)
        user = User(
            email=raw_user['email'],
            username=raw_user['username']
        )
        user.set_password(raw_user['password'])
        user.save()
        Token.objects.create(user=user)
        Passenger.objects.create(user=user, **request.data)
        return Response(data={"message": 'passenger created'}, status=status.HTTP_201_CREATED)

        # ToDo Create email confirmation logic

        # current_site = get_current_site(request)
        # subject = f'Dear {user.first_name}. Activate Your Account'
        # message = render_to_string('account_activation_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        # user.email_user(subject, message)
        #
        # return Response(data={"message": f"Email confirmation sent to {user.email}"}, status=status.HTTP_201_CREATED)


class Logout(APIView):

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)