from django.db import models

# Create your models here.
class Trip(models.Model):
    trip_organizer = models.CharField(max_length=50)
    attending = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    budget = models.IntegerField()
    date = models.DateField()
    plan = models.TextField(max_length=250)
    notes = models.TextField(max_length=250)

    def __str__(self):
        return self.location
