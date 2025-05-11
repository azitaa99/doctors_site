from django.urls import path
from .views import Hello, DrProfile,RegisterationView,LoginView,LogoutView,PanelView,ChangePassView



app_name='accounts'

urlpatterns = [
    path('', Hello.as_view(), name='hello'),
    path('profile/<int:doctor_id>',DrProfile.as_view(), name='dr_profile'),
    path('register/',RegisterationView, name='register_page'),
    path('login/',LoginView, name='login_page'),
    path('logout/',LogoutView, name='logout_page'),
    path('panel/',PanelView, name='panel_page'),
    path('changepass/',ChangePassView, name='changepass_page'),
      







]
