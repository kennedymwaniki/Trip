from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()


class Trip(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=3)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField()
    owner = models.ForeignKey(
        User, related_name='trips', on_delete=models.CASCADE)

    def __str__(self):
        return self.city


class Note(models.Model):
    EXCURSIONS = (('museum', 'Museum'), ('restaurant', 'Restaurant'),
                  ('park', 'Park'),
                  ('dining', 'Dining'), ('General', 'general'), ('shopping', 'Shopping'), ('event', 'Event'))
    name = models.CharField(max_length=100)
    description = models.TextField()
    trip = models.ForeignKey(Trip, related_name='notes',
                             on_delete=models.CASCADE)
    type = models.CharField(
        max_length=100, choices=EXCURSIONS, default='General')
    img = models.ImageField(upload_to='notes', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.name} in {self.trip.city}"
