from .models import FareConditionPrice, Flight, Seat
import geopy.distance


def calculate_total_amount(flight: Flight, seat: Seat) -> float:
    """Calculate flight price"""

    coef = float(FareConditionPrice.objects.get(fare_condition=seat.fare_condition).coef)
    coords_1 = (
        flight.departure_airport.address.lat,
        flight.departure_airport.address.lon,
    )
    coords_2 = (
        flight.arrival_airport.address.lat,
        flight.arrival_airport.address.lon
    )

    distance = geopy.distance.distance(coords_1, coords_2).km

    return float(distance * coef)
