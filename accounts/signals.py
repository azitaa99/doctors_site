from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyUser
from doctors.models import Doctors,specialits



@receiver(post_save,sender=MyUser)
def create_user_doctor(sender,instance, created,**kwargs):
    if created and instance.user_type == 'doctor':
        speciality=specialits.objects.get(name='عمومی')
        Doctors.objects.create(
            user=instance,
            speciality=speciality
        )
