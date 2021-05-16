from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django_filters import rest_framework as filters
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db import models

from .models import *
from .serializers import *

from base.tokens import account_activation_token


class AirportView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class PassengerView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('user__email', )


class ModelView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class AircraftView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer


class AddressView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class FlightView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class SeatView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class TicketView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        return self.queryset.filter(passenger=self.request.user.passenger)


class Signup(generics.CreateAPIView):
    """
    Register User
    """
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):

        raw_user = request.data.pop("user")
        if User.objects.filter(models.Q(email=raw_user.get('email')) | models.Q(username=raw_user.get('username'))).exists():
            return Response(
                data={
                    "message": f"User with email {raw_user.get('email')} already exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(is_active=False, **raw_user)
        Token.objects.create(user=user)
        Passenger.objects.create(user=user, **request.data)

        return Response(status=status.HTTP_201_CREATED)

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

