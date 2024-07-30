import datetime

from django.core.mail.backends import console

from .models import *
from django.forms import ModelForm, TextInput, Textarea, DateInput, TimeInput, Select, HiddenInput, NumberInput


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['master', 'time', 'date', 'service']

        widgets = {
            "master": Select(attrs={

                'class': 'form-control',
                'placeholder': 'Грумер'
            }),
            "service": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Услуга'
            }),
            "time": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Время',

            }),
            "date": DateInput(attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control',
                'min': datetime.date.today(),
                'max': datetime.date.today() + datetime.timedelta(days=14),

            })}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time'].queryset = Record.objects.none().values_list('time', flat=True)

        if 'date_id' in self.data:
            try:
                date_id = int(self.data.get('date_id'))
                master_id = int(self.data.get('master_id'))
                times = Record.objects.filter(master=master_id).filter(date=date_id).values_list('time', flat=True)
                available_times = []
                for time in CHOISE_TIME:
                    if time not in times:
                        available_times.append(time)
                self.fields['time'] = available_times
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset


class RegPetForm(ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'race', 'age', 'type', 'photo')
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кличка'
            }),
            "race": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Порода'
            }),
            "age": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Возраст (полных лет)'
            }),
            "type": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Тип'
            }),

        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['race'].queryset = Race.objects.none()
            if 'type' in self.data:
                try:
                    type_id = int(self.data.get('type'))
                    self.fields['race'].queryset = Race.objects.filter(type=type_id)
                except (ValueError, TypeError):
                    pass


class RecordChangeStatus(ModelForm):
    class Meta:
        model = Record
        fields = ['status']
        widgets = {
            "status": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Статус'
            })
        }


class PetChangeInf(ModelForm):
    class Meta:
        model = Pet
        fields = ('name', 'race', 'age', 'type', 'photo')
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кличка'
            }),
            "race": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Порода'
            }),
            "age": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Возраст (полных лет)'
            }),
            "type": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Тип',
            }),
        }


class ChangeServ(ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'price', 'description', 'type')
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Стоимость'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            "type": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Тип животного'
            }),
        }


class CreateGroomer(ModelForm):
    class Meta:
        model = Employee
        fields = ('fam', 'name', 'otch', 'exp', 'about', 'photo')
        widgets = {
            "fam": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "otch": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество'
            }),
            "exp": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Опыт работы (полных лет)'
            }),
            "about": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'О себе',
            }),
        }


class ChangeGroomer(ModelForm):
    class Meta:
        model = Employee
        fields = ('fam', 'name', 'otch', 'exp', 'about', 'photo')
        widgets = {
            "fam": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "otch": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество'
            }),
            "exp": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Опыт работы (полных лет)'
            }),
            "about": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'О себе',
            }),
        }


class CreateServ(ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'price', 'description', 'type')
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            "price": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Стоимость'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            "type": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Тип животного'
            }),

        }
