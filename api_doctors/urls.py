from django.urls import path
from .views import AvailableDaysApiView,AvailableTimeApiView,RegisterApiView,ReserveTimeApiView, LogoutApiView,LoginApiView,UserInfoApiView,UserAppointmentsApiView,UserAChangePass
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


app_name='api_dr'

urlpatterns=[
    path('api/doctor/<int:doctor_id>/available_day/',AvailableDaysApiView.as_view(), name='api_available'),
    path('api/doctor/<int:doctor_id>/available_times/<str:date>/',AvailableTimeApiView.as_view(), name='api_available_time'),
    path('api/reserve_time/', ReserveTimeApiView.as_view(), name='reserve_time'),
    path('api/register/',RegisterApiView.as_view(), name='register_api'),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/logout/', LogoutApiView.as_view(), name='logout_api'),
    path('api/login/', LoginApiView.as_view(), name='login_api'),
    path('api/user-info/', UserInfoApiView.as_view(), name='user_info'),
    path('api/user-appointments/', UserAppointmentsApiView.as_view(), name='user_appointments'),
    path('api/user-changepassword/', UserAChangePass.as_view(), name='user_changepass'),



]