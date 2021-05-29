from transportation.models import Aircraft, Seat


def generate_seats():
    """Generate seats for aircrafts"""

    aircrafts = Aircraft.objects.all()
    for aircraft in aircrafts:
        for seat_no in range(138):
            if seat_no < 46:
                fare_cond = 'economy'
            elif 46 <= seat_no < 92:
                fare_cond = 'comfort'
            else:
                fare_cond = 'business'
            Seat.objects.create(aircraft=aircraft, seat_no=seat_no, fare_condition=fare_cond)
