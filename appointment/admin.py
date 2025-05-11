from django.contrib import admin
from .models import Appointment,TimeSlot
from .forms import AppointmentForm



admin.site.register(TimeSlot)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    form=AppointmentForm
   