from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class MyUser(AbstractBaseUser):
    USER_TYPE_CHOICES=(('doctor','پزشک'),('patient','بیمار'),('admin','مدیر'))
    user_type=models.CharField(verbose_name='نوع کاربر',max_length=10,choices=USER_TYPE_CHOICES,default='patient')
    phone=models.CharField(max_length=11,unique=True,verbose_name='موبایل')
    email=models.EmailField(max_length=255,unique=True,verbose_name='ایمیل')
    full_name=models.CharField(max_length=400, verbose_name='نام کامل')
    
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)

    objects=UserManager()

    USERNAME_FIELD='phone'
    REQUIRED_FIELDS=['email','full_name']

    def __str__(self):
        return f'{self.full_name}'
    
    def get_full_name(self):
        return f'{self.full_name}' 



    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural=' کاربران'
    
    

