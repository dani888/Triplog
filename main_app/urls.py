from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('upcomingtrips/', views.upcomingtrips_index, name='index'),
    path('pasttrips/', views.pasttrips_index, name='indexpast'),
    path('upcomingtrips/<int:trip_id>/', views.trips_detail, name='detail'),
    path('pasttrips/<int:trip_id>/', views.pasttrips_detail, name='pastdetail'),
    path('upcomingtrips/create/', views.TripCreate.as_view(), name='trips_create'),
    path('upcomingtrips/<int:pk>/update/', views.TripUpdate.as_view(), name='trips_update'),
    path('upcomingtrips/<int:pk>/delete/', views.TripDelete.as_view(), name='trips_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('upcomingtrips/<int:trip_id>/add_photo/', views.add_photo, name='add_photo'),
    path('upcomingtrips/<int:trip_id>/add_comment/', views.add_comment, name='add_comment'),
    path('pasttrips/<int:trip_id>/add_comment/', views.add_comment, name='add_comment'),
]
