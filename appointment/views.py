from django.shortcuts import render
from .models import  TimeSlot
from dal import autocomplete



class timeslotautocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs=TimeSlot.objects.filter(is_booked=False)
        doctor_id=self.forwarded.get('doctor', None)
        if doctor_id:
            qs=qs.filter(doctor_id=doctor_id)
        return qs
