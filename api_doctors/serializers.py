from rest_framework import serializers
from appointment.models import TimeSlot
from accounts.models import MyUser





class AvailableDaySerializer(serializers.Serializer):
    weekday=serializers.CharField()
    date=serializers.DateField()
 
class AvailableTimeSerializer(serializers.ModelSerializer):
    start_time=serializers.SerializerMethodField()
    class Meta:
        model=TimeSlot
        fields=['start_time', 'id']

    def get_start_time(self, obj):
        return obj.start_time.strftime('%H:%M')
   




class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=MyUser
        fields=['full_name', 'email', 'phone','user_type','password','confirm_password']


    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('پسورد های وارد شده یکسان نیست')
        return data
    

    def validate_email(self ,value):
        user=MyUser.objects.filter(email=value).exists()
        if user :
            raise serializers.ValidationError('ایمیل وارد شده قبلا ثبت شده')
        return value
    

    def create(self, validated_data):

        validated_data.pop('confirm_password')
        password=validated_data.pop('password')
        user=MyUser(**validated_data)
        user.set_password(password)
        user.save()
        return user




