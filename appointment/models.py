from django.db import models
from doctors.models import Doctors
from accounts.models import MyUser
from django.core.exceptions import ValidationError





class Appointment(models.Model):
    doctor=models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name='appoinments')
    patient=models.ForeignKey(MyUser,on_delete=models.CASCADE,limit_choices_to={'user_type':'patient'},related_name='p_appointments')
    slot=models.ForeignKey('TimeSlot',on_delete=models.CASCADE,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=('slot','doctor')
    
        verbose_name='وقت ویزیت'
        verbose_name_plural=' وقت های ویزیت'



    def clean(self):
        if self.slot.doctor != self.doctor :
            raise ValidationError('وقت انتخابی مربوط به پزشک مورد نظر نیست')
        if self.slot.is_booked == True:
            raise ValidationError('وقت مورد نظر قبلا رزرو شده')
        

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save( *args, **kwargs)
        self.slot.is_booked= True
        self.slot.save()



    

    
    def __str__(self):
        return f'{self.patient.email} دارای وقت ویزیت با دکتر  {self.doctor} در {self.slot.date.strftime("%y-%m-%d %H:%M")}'    




class TimeSlot(models.Model):
    doctor=models.ForeignKey(Doctors,on_delete=models.CASCADE, related_name='time_slots')
    date=models.DateField(verbose_name='تاریخ نوبیت')
    start_time=models.TimeField(verbose_name='ساعت شروع')
    end_time=models.TimeField(verbose_name='ساعت پایان')
    is_booked=models.BooleanField(default=False, verbose_name='رزرو /آزاد')

    class Meta:
        unique_together=('doctor','date','start_time')
        ordering=['date','start_time']
        verbose_name='زمان نوبت'
        verbose_name_plural='زمان های نوبت'

    def __str__(self):
        return f'{self.doctor} | {self.date} | {self.start_time.strftime("%H : %M ")} - {self.end_time.strftime("%H : %M")}'