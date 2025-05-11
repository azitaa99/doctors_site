from django import forms
from django.core.exceptions import ValidationError

from .models import MyUser





from django import forms
from django.core.exceptions import ValidationError
from accounts.models import MyUser

class RegistrationForm(forms.Form):
    USER_TYPE_CHOICES = (('doctor', 'پزشک'), ('patient', 'بیمار'))

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label='نوع کاربر')
    full_name = forms.CharField(max_length=200, label='نام کامل', required=True)
    phone = forms.CharField(max_length=11, label='موبایل', required=True)
    email = forms.EmailField(max_length=255, label='ایمیل', required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}),
        label='پسورد'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'}),
        label='تکرار پسورد'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise ValidationError('پسورد وارد شده یکسان نیست')
        return cd

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            raise ValidationError('ایمیل وارد شده قبلا ثبت شده')
        return email










class LoginForm(forms.Form):
    phone=forms.CharField(max_length=200, label='موبایل')
    password=forms.CharField(max_length=200,label='پسورد')