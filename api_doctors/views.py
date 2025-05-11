from django.shortcuts import render
from rest_framework.views import APIView
from appointment.models import TimeSlot, Appointment
import datetime
from .serializers import AvailableDaySerializer, AvailableTimeSerializer,UserRegisterSerializer
from rest_framework.response import Response
from doctors.models import DoctorWeeklySchedule, Doctors
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import permissions, status
from accounts.models import MyUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from rest_framework.exceptions import ValidationError



class AvailableDaysApiView(APIView):
    def get(self, request,doctor_id):
        now=datetime.datetime.now()
        today=now.date()
        doctor=Doctors.objects.get(id=doctor_id)


        slots=doctor.time_slots.filter(
            date__gte=today
        )

        weekday_translation={
            'Saturday':'شنبه',
            'Sunday':'یکشنبه',
            'Monday':'دوشنبه',
            'Tuesday':'سه شنبه',
            'Wednesday':'چهارشنبه',
            'Thursday':'پنج شنبه'
        }
        
        
        
        days={}
        for slot in slots:
            weekday_en=slot.date.strftime('%A')
            weekday_fa=weekday_translation.get(weekday_en,weekday_en)
            if slot.date not in days:
                days[slot.date]={
                    'weekday':weekday_fa,
                    'date':slot.date.strftime('%Y-%m-%d')
                }
        ser_slots=AvailableDaySerializer(instance=days.values(), many=True)
        return Response(ser_slots.data)
    



class AvailableTimeApiView(APIView):
    def get(self, request,doctor_id, date):
        slots=TimeSlot.objects.filter(
            doctor_id=doctor_id,
            date=date,
            is_booked=False  
        )
    
        ser_data=AvailableTimeSerializer(slots, many=True)
        return Response(ser_data.data)
  





class RegisterApiView(APIView):
    def post(self, request):
        ser_data=UserRegisterSerializer(data=request.data)
     
        if ser_data.is_valid():
            ser_data.save()
            return Response ({'message':'ثبت نام انجام شد'},status=200)
      
        return Response(ser_data.errors, status=400)
    



from django.core.exceptions import ValidationError

class ReserveTimeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        patient = request.user
        time_slot_id = request.data.get('time_slot_id')
        doctor_id = request.data.get('doctor_id')

        if not time_slot_id or not doctor_id:
            return Response({'error': 'شناسه زمان و پزشک الزامی است'}, status=400)

        try:
            slot = get_object_or_404(TimeSlot, id=time_slot_id, doctor_id=doctor_id, is_booked=False)
        except TimeSlot.DoesNotExist:
            return Response({'error': 'زمان مورد نظر یا پزشک یافت نشد یا قبلاً رزرو شده است.'}, status=400)

        try:
            appointment = Appointment(
                doctor=slot.doctor,
                patient=patient,
                slot=slot
            )
            appointment.full_clean() 
            appointment.save()
            return Response({'message': 'وقت شما با موفقیت رزرو شد'})
        except ValidationError as ve:
            return Response({'error': ve.message_dict}, status=400)
        except Exception as e:
            return Response({'error': f'خطا در رزرو وقت: {str(e)}'}, status=500)





class LogoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginApiView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if not phone or not password:
            return Response({'detail': 'شماره تلفن و رمز عبور الزامی هستند'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            return Response({'detail': 'کاربری با این شماره تلفن یافت نشد'}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({'detail': 'رمز عبور اشتباه است'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'auth_token': str(refresh.access_token),
            'access': str(refresh.access_token),
        })
        
        
        
        
class UserInfoApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'phone': user.phone,
            'name': user.get_full_name(),
            'email': user.email,
        })
        
        
        
class UserAppointmentsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        appointment_data = []
        user=request.user
        if user.user_type == 'patient':
            
            appointments=user.p_appointments.all()
        elif user.user_type == 'doctor':
            appointments=Appointment.objects.filter(doctor__user=user)
        if not appointments:
            return Response({"message": "هیچ نوبتی برای شما یافت نشد."})
        for appoint in appointments:
            
            appointment_data.append({
                'doctor_name': appoint.doctor.user.get_full_name(),
                'date': appoint.slot.date.strftime('%Y-%m-%d'),
                'time': appoint.slot.start_time.strftime('%H:%M')
                
            }  
             )
        return Response(appointment_data)
    
    
    
    
class UserAChangePass(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user=request.user
        old_password=request.data.get('old_password')
        new_password=request.data.get('new_password')
        confirm_new_password=request.data.get('confirm_new_password')
        if new_password != confirm_new_password:
            return Response({'detail': 'رمزهای جدید یکسان نیستند'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(old_password) :
            return Response({'detail':'رمز عبور قدیمی صحیح نیست'}, status=status.HTTP_400_BAD_REQUEST)
         
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({"message": "رمز عبور با موفقیت تغییر یافت."}, status=status.HTTP_200_OK)