from django.shortcuts import render, redirect
from django.views import View
from doctors.models import Doctors, MyUser
from django.http import JsonResponse
from appointment.models import Doctors, TimeSlot
import datetime
from  django.views.generic import DetailView, View
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages





class Hello(View):
    def get(self,request):
        doctors=Doctors.objects.all()
        return render(request,'accounts/hello.html',{'doctors':doctors})




class DrProfile(DetailView):

    model = Doctors

    template_name = 'accounts/profile.html'

    context_object_name = 'doctor'

    pk_url_kwarg='doctor_id'








# class RegisterationView(View):

#     form_class=RegistrationForm
#     template_name='accounts/register.html'
#     def get(self, request):
#         form=self.form_class()
#         return render(request,self.template_name,{'form':form})




#     def post(self, request ):
#         form=self.form_class(request.POST)
        
#         if form.is_valid():
#             cd=form.cleaned_data
#             user=MyUser.objects.create_user(
#                 phone=cd['phone'],
#                 email=cd['email'],
#                 full_name=cd['full_name'],
#                 password=cd['password'],
#                 user_type=cd['user_type']
               
     
#             )
           
#             user.save()
#             return redirect('accounts:hello')
#         return render(request, self.template_name, {'form':form})





# class LoginView(View):
#     form_class=LoginForm
#     template_name='accounts/login.html'
#     def get(self,request):
#         return render(request,self.template_name,{'form':self.form_class})


#     def post(self,request):
#         form=self.form_class(request.POST)
#         if form.is_valid():
#             cd=form.cleaned_data
#             user=authenticate(request,username=cd['username'],password=cd['password'])
#             if user is not None:
#                 login(request,user)
#                 messages.success(request,'خوشامدید',extra_tags='success')
#                 return redirect('accounts:hello')
#             messages.error(request,'موبایل یا پسورد اشتباه است','danger')
#             return render(request,self.template_name,{'form':self.form_class})
            
    

# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         messages.success(request,'از حساب کاربری خود خارج شدید','success')
#         return redirect('accounts:hello')







def LoginView(request):
    return render(request, 'accounts/login.html')

def RegisterationView(request):
    return render(request, 'accounts/register.html')

def LogoutView(request):
    return render(request, 'accounts/logout.html')
def PanelView(request):
    return render(request, 'accounts/panel.html')

def ChangePassView(request):
    return render(request,'accounts/change_password.html')
