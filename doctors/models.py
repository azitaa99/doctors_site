from django.db import models
from accounts.models import MyUser


class specialits(models.Model):

    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='تخصص'
        verbose_name_plural='تخصص ها'
    

class Doctors(models.Model):
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE,related_name='dr_profile',null=False,limit_choices_to={'user_type':'doctor'})
    speciality=models.ForeignKey(specialits, on_delete=models.CASCADE,related_name='doctors',blank=True,null=True, default=None)
    image=models.ImageField(upload_to='doctors/%y-%m/', null=True, blank=True)
    available=models.BooleanField(default=True)
    def __str__(self):
        return self.user.full_name
    class Meta:
        verbose_name='پزشک'
        verbose_name_plural='پزشکان'
    

class DoctorWeeklySchedule(models.Model):
    WEEK_DAYS=[
        ('sat','شنبه'),
        ('sun','یکشنبه'),
        ('mon','دوشنبه'),
        ('tue','سه شنبه'),
        ('wed','چهارشنبه'),
        ('thu','پنج شنبه')
    ]
    doctor=models.ForeignKey(Doctors,on_delete=models.CASCADE,related_name='availabls')
    day_of_week=models.CharField(max_length=50, choices=WEEK_DAYS)
    start_time=models.TimeField()
    end_time=models.TimeField()
    visit_duration=models.PositiveBigIntegerField(help_text='مثلا 20 دقیقه')


    def __str__(self):
        return f'{self.doctor}'
    

    class Meta:
        verbose_name='برنامه'
        verbose_name_plural=' برنامه ها'
    