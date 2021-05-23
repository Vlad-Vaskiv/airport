from transportation.models import *
from .code_generator import id_generator


def generate_flights():
    flight_no = id_generator(size=6)
