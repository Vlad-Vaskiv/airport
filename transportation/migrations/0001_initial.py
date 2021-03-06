# Generated by Django 3.2.3 on 2021-05-16 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('line', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('timezone', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('range', models.PositiveIntegerField(help_text='Maximum flight range, km')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transportation.address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('flight_no', models.CharField(max_length=6)),
                ('scheduled_departure', models.DateTimeField()),
                ('scheduled_arrival', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('on_time', 'On Time'), ('delayed', 'Delayed'), ('departed', 'Departed'), ('arrived', 'Arrived'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20)),
                ('actual_departure', models.DateTimeField(blank=True, null=True)),
                ('actual_arrival', models.DateTimeField(blank=True, null=True)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transportation.aircraft')),
                ('arrival_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='arr_flights', to='transportation.airport')),
                ('departure_airport', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dep_flights', to='transportation.airport')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='models')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number', models.CharField(max_length=20)),
                ('birthday', models.DateField()),
                ('phone', models.CharField(max_length=15)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seat_no', models.IntegerField()),
                ('fare_condition', models.CharField(choices=[('economy', 'Economy'), ('comfort', 'Comfort'), ('business', 'Business')], max_length=10)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transportation.aircraft')),
            ],
            options={
                'unique_together': {('aircraft_id', 'seat_no')},
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='transportation.flight')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='transportation.passenger')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transportation.seat')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='aircraft',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transportation.model'),
        ),
        migrations.AddConstraint(
            model_name='flight',
            constraint=models.CheckConstraint(check=models.Q(('scheduled_arrival__gte', django.db.models.expressions.F('scheduled_departure'))), name='greater_check'),
        ),
        migrations.AlterUniqueTogether(
            name='flight',
            unique_together={('flight_no', 'scheduled_departure')},
        ),
    ]
