from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number')


class CustomUserChangeInf(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('surname', 'name', 'phone_number')
        widgets = {
            "surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "phone_number": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            }),
        }


