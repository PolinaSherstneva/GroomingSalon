from django.db import models
from Users.models import *

# Create your models here.
CHOISE_TIME = {
    "09:00": "09:00",
    "10:00": "10:00",
    "11:00": "11:00",
    "12:00": "12:00",
    "13:00": "13:00",
    "14:00": "14:00",
    "15:00": "15:00",
    "16:00": "16:00",
    "17:00": "17:00",
}

STATUS_CHOISE = {
    "1": "Ожидание подтверждения",
    "2": "Запись подтверждена",
    "3": "Выполнена",
    "4": "Отменена",
}


class TypeAnimal(models.Model):
    type = models.CharField(max_length=15, default="Собака")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Race(models.Model):
    name_race = models.CharField(max_length=100)
    type = models.ForeignKey(TypeAnimal, on_delete=models.CASCADE, default=1, blank=True)

    def __str__(self):
        return self.name_race

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    type = models.ForeignKey(TypeAnimal, on_delete=models.CASCADE)
    photo = models.ImageField(default="", blank=True, upload_to="pets")

    def __str__(self):
        return self.race.name_race + " " + self.name

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1000)
    type = models.ForeignKey(TypeAnimal, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + str(self.price)+"р"

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Employee(models.Model):
    fam = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    otch = models.CharField(max_length=50)
    exp = models.CharField(max_length=50)
    photo = models.ImageField(default="", blank=True, upload_to="groomers")
    about = models.TextField(default="", blank=True, max_length=1000)

    def __str__(self):
        return self.fam + " " + self.name + " " + self.otch

    class Meta:
        verbose_name = "Грумер"
        verbose_name_plural = "Грумеры"


class Portfolio(models.Model):
    employee = models.ForeignKey(Employee, default="1", related_name="employee", on_delete=models.CASCADE)
    photo = models.ImageField(default="")
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.employee.fam + " " + self.employee.name + " " + self.description

    class Meta:
        verbose_name = "Портфолио"
        verbose_name_plural = "Портфолио"


class PetAndUser(models.Model):
    pet = models.ForeignKey(Pet, default="1", related_name="pet", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, default="1", related_name="user", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.surname + " - " + self.pet.name

    class Meta:
        verbose_name = "Клиент и питомец"
        verbose_name_plural = "Клиенты и питомцы"


class Record(models.Model):
    pet_user = models.ForeignKey(PetAndUser, default="1", on_delete=models.CASCADE)
    master = models.ForeignKey(Employee, default="1", on_delete=models.CASCADE)
    time = models.CharField(max_length=50, choices=CHOISE_TIME)
    date = models.DateField()
    service = models.ForeignKey(Service, default="1", on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOISE)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"





