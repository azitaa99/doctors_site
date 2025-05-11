from dal import autocomplete
from django import forms
from .models import Appointment




class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment
        fields='__all__'
        widgets={
            'slot':autocomplete.ModelSelect2(url='appointment:timeslot-autocomplete', forward=['doctor']),
        }