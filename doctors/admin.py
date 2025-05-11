from django.contrib import admin
from . models import Doctors, specialits,DoctorWeeklySchedule
from django.contrib.auth.admin import UserAdmin



class WeeklyScheduleINLINE(admin.StackedInline):
    model=DoctorWeeklySchedule
    can_delete=True





class ExtendedDoctorAdmin(admin.ModelAdmin):
    inlines=(WeeklyScheduleINLINE,)
    search_fields=('user__full_name',)
   





admin.site.register(Doctors,ExtendedDoctorAdmin)

admin.site.register(specialits)
