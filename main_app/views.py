from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Trip

# Create your views here.
from django.http import HttpResponse

# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def upcomingtrips_index(request):
  trips = Trip.objects.all()
  return render(request, 'trips/index.html', { 'trips': trips })

def trips_detail(request, trip_id):
  trip = Trip.objects.get(id=trip_id)
  return render(request, 'trips/detail.html', { 'trip': trip })

class TripCreate(CreateView):
  model = Trip
  fields = '__all__'
  success_url = '/upcomingtrips/'

# class Trip:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, First_name, Last_name, vaccinated, location, date, Past_trip, images, review):
#     self.First_name = First_name
#     self.Last_name = Last_name
#     self.vaccinated = vaccinated
#     self.location = location
#     self.date = date
#     self.Past_trip = Past_trip
#     self.images = images
#     self.review = review

# trips = [
#   Trip('Dan', 'Werm', True, 'Germany', 'Nov-12-2022', False, None, None),
# #   Trip('Sachi', 'tortoise shell', 'diluted tortoise shell', 0),
# #   Trip('Raven', 'black tripod', '3 legged cat', 4)
# ]
