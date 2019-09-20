from django.urls import path
from .views import *


app_name = "app"
urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('search/', SearchResultsView.as_view(), name="search_results"),
	path('events/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('events/create/new', EventCreate.as_view(), name='event_create'),
    path('events/update/<slug:slug>/', EventUpdate.as_view(), name='event_update'),
    path('events/delete/<slug:slug>/', EventDelete.as_view(), name='event_delete'),
]
