from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Appointment,TimeSlot
from doctors.models import DoctorWeeklySchedule, Doctors
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta










@receiver(post_save, sender=DoctorWeeklySchedule)
def create_slots(sender,instance,created, **kwargs):
    days_ahead=14
    today=datetime.today().date()
    target_day=instance.day_of_week.lower()

    for d in range(days_ahead):
        current_date=today +timedelta(days=d)
        if current_date.strftime('%a').lower() == target_day:
            start=datetime.combine(current_date,instance.start_time)
            end=datetime.combine(current_date,instance.end_time)
            visit_duration=timedelta(minutes=instance.visit_duration)
            while start + visit_duration <= end :
                TimeSlot.objects.get_or_create(doctor=instance.doctor,date=current_date,start_time=start.time(),end_time=(start+visit_duration).time())
                start += visit_duration











   



