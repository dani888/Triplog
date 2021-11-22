from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
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
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class TripUpdate(UpdateView):
  model = Trip
  fields = '__all__'

class TripDelete(DeleteView):
  model = Trip
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
