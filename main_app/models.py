from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

# Create your models here.
class Trip(models.Model):
    trip_organizer = models.CharField(max_length=50)
    attending = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    budget = models.IntegerField()
    date = models.DateField()
    plan = models.TextField(max_length=250)
    notes = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

    def get_absolute_url(self):
        return reverse('detail', kwargs={'trip_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for trip_id: {self.trip_id} @{self.url}"