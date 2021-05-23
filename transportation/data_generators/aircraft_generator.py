import random
import csv
from transportation.models import Aircraft, Seat, Model
from .code_generator import id_generator


def generate_models():
    with open('transportation/data_generators/aircraft_db.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            yield Model.objects.create(name=row.get('type'))


def generate_aircraft():
    for model in generate_models():
        code = id_generator()
        model_range = random.randint(3850, 8385)
        Aircraft.objects.create(code=code, model=model, range=model_range)
