from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('upcomingtrips/', views.upcomingtrips_index, name='index'),
    path('upcomingtrips/<int:trip_id>/', views.trips_detail, name='detail'),
    path('upcomingtrips/create/', views.TripCreate.as_view(), name='trips_create'),
]
