from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()

router.register("airport", views.AirportView)
router.register("passenger", views.PassengerView)
router.register("model", views.ModelView)
router.register("aircraft", views.AircraftView)
router.register("address", views.AddressView)
router.register("flight", views.FlightView)
router.register("seat", views.SeatView)
router.register("ticket", views.TicketView)
# router.register('price', views.PriceView, basename='get_price')

urlpatterns = [path("", include(router.urls)), path("price", views.PriceView.as_view())]
