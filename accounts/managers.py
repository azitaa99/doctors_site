from django.contrib.auth.models import BaseUserManager




class UserManager(BaseUserManager):

    def create_user(self,phone,email,full_name=None,password=None,user_type=None):
        if not phone:
            raise ValueError('user must have phone')
        if not email:
            raise ValueError('user must have email')
       
        

        user=self.model(phone=phone, email=self.normalize_email(email),full_name=full_name,user_type=user_type)
        user.set_password(password)
        user.save(using=self.db)
        return user


    def create_superuser(self, phone, email,full_name=None,password=None,user_type=None):

        user=self.create_user(phone,email,full_name,password,)
 


        user.is_superuser=True
        user.is_staff=True
        user.user_type='admin'
        user.save(using=self._db)

        return user 
 