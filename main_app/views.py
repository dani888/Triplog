from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Trip, Photo
from datetime import date
from .forms import CommentForm
import uuid
import boto3


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-photo-uploadan'


# Create your views here.
from django.http import HttpResponse

# Define the home view
def home(request):
  userz = request.user
  print(userz)
  return render(request, 'home.html', {'user': userz})

def about(request):
  return render(request, 'about.html')

def handler404(request):
    return render(request, '404.html', status=500)

@login_required
def search_trips(request):
  if request.method == "POST":
    searched = request.POST['searched']
    trips = Trip.objects.filter(location__icontains=searched).filter(user=request.user)
    return render(request, 'trips/search_trips.html', {'searched': searched, 'trips': trips })

@login_required
def upcomingtrips_index(request):
  userz = request.user
  today = date.today()
  trips = Trip.objects.filter(user=request.user).filter(date__gte=today)
  return render(request, 'trips/index.html', { 'trips': trips, 'user': userz })


@login_required
def pasttrips_index(request):
  today = date.today()
  trips = Trip.objects.filter(user=request.user).filter(date__lte=today)
  return render(request, 'trips/indexpast.html', { 'trips': trips })

@login_required
def publictrip_index(request):
  trips = Trip.objects.filter(public='Y')
  return render(request, 'trips/indexpublic.html', { 'trips': trips })

@login_required
def trips_detail(request, trip_id):
  userz = request.user
  trip = Trip.objects.filter(user=request.user).get(id=trip_id)
  comment_form = CommentForm()
  return render(request, 'trips/detail.html', { 'trip': trip, 'comment_form': comment_form, 'user': userz})

@login_required
def pasttrips_detail(request, trip_id):
  userz = request.user
  trip = Trip.objects.filter(user=request.user).get(id=trip_id)
  comment_form = CommentForm()
  return render(request, 'trips/pastdetail.html', { 'trip': trip, 'comment_form': comment_form, 'user': userz})

@login_required
def publictrips_detail(request, trip_id):
  userz = request.user
  trip = Trip.objects.filter(public='Y').get(id=trip_id)
  comment_form = CommentForm()
  return render(request, 'trips/publicdetail.html', { 'trip': trip, 'comment_form': comment_form, 'user': userz})


@login_required
def add_photo(request, trip_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, trip_id=trip_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', trip_id=trip_id)


class TripCreate(LoginRequiredMixin, CreateView):
  model = Trip
  fields = ['trip_organizer', 'attending', 'location', 'budget', 'date', 'plan', 'notes', 'public']
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
      return redirect('')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def add_comment(request, trip_id):
  userz = request.user.id
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.trip_id = trip_id
    new_comment.user_id = userz
    new_comment.save()
  return redirect('detail', trip_id=trip_id)

@login_required
def add_commentpublic(request, trip_id):
  userz = request.user.id
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.trip_id = trip_id
    new_comment.user_id = userz
    new_comment.save()
  return redirect('public_detail', trip_id=trip_id)

class TripUpdate(LoginRequiredMixin, UpdateView):
  model = Trip
  fields = ['trip_organizer', 'attending', 'location', 'budget', 'date', 'plan', 'notes', 'public']

class TripDelete(LoginRequiredMixin, DeleteView):
  model = Trip
  success_url = '/upcomingtrips/'
