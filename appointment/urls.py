from django.urls import path
from .views import  timeslotautocomplete

app_name='appointment'

urlpatterns=[
    path('timeslot-autocomplete/',timeslotautocomplete.as_view(), name='timeslot-autocomplete')
]