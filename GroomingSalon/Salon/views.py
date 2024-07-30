import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from Users.models import CustomUser
from Salon.models import Service
from Salon.forms import *
from Users.models import *


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


def main(request):
    return render(request, 'Salon/Main.html')


def services(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = CustomUser.objects.get(phone_number=request.user.phone_number)
    query = request.GET.get('search')
    if query is None:
        services = Service.objects.all()
    else:
        services = Service.objects.filter(Q(name__iregex=query) | Q(price__icontains=query) | Q(description__iregex=query))
    return render(request, 'Salon/Services.html', {'services': services, 'user_profile': user_profile})


def lk(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = CustomUser.objects.get(phone_number=request.user.phone_number)
    pets = PetAndUser.objects.filter(user=request.user)
    records = Record.objects.filter(pet_user__user=request.user).exclude(status=3).order_by("-date", "time")
    context = {'user_profile': user_profile, 'pets': pets, 'records': records}
    if request.user.is_superuser:
        return redirect('administration')
    return render(request, 'Salon/LK.html', context)


def archive_lk(request):
    user_profile = request.user
    records = Record.objects.filter(pet_user__user=request.user).order_by("-date", "time")
    context = {'user_profile': user_profile, 'records': records}
    return render(request, 'Salon/Archive.html', context)


def portfolio(request, master_id):
    master = Employee.objects.get(id=master_id)
    portfolios = Portfolio.objects.filter(employee=master)

    context = {'master': master, 'portfolios': portfolios}

    return render(request, 'Salon/Portfolio.html', context)


def reg_pet(request):
    form = RegPetForm(request.POST)
    form.fields['race'].queryset = Race.objects.order_by("name_race")
    if request.method == 'POST':
        form = RegPetForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            race = form.cleaned_data['race']
            age = form.cleaned_data['age']
            photo = form.cleaned_data['photo']
            type = form.cleaned_data['type']
            pet = Pet.objects.create(
                name=name,
                race=race,
                age=age,
                type=type,
                photo=photo)
            user = CustomUser.objects.get(phone_number=request.user.phone_number)
            pet_user = PetAndUser.objects.create(pet=pet, user=user)
            pet_user.save()
            return render(request, 'Salon/Reg-pet-ready.html')
    return render(request, 'Salon/Reg-pet.html', {'form': form})


def load_race(request):
    type_id = request.GET.get('type_id')
    races = Race.objects.filter(type=type_id).order_by("name_race")
    return render(request, 'Salon/ajax-race.html', {'races': races})


# Администрирование >

def administration(request):
    records = Record.objects.all().exclude(status=3).order_by("-date", "time")
    query = request.GET.get('search')
    date = request.GET.get('date')
    if query or date is not None:
        if query is not None:
            records = records.filter(
                Q(pet_user__user__surname__iregex=query) | Q(pet_user__user__name__iregex=query) |
                Q(pet_user__user__phone_number__iregex=query) | Q(pet_user__pet__name__iregex=query) |
                Q(service__name__iregex=query) | Q(master__fam__iregex=query) |
                Q(master__name__iregex=query) | Q(master__otch__iregex=query)).order_by("-date", "time")
        if date is not None:
            if date == "increasing":
                records = records.order_by("-id", "-date", "time")
            else:
                records = records.order_by("id", "date", "time")
        if query and date is not None:
            records = records.filter(
                Q(pet_user__user__surname__iregex=query) | Q(pet_user__user__name__iregex=query) |
                Q(pet_user__user__phone_number__iregex=query) | Q(pet_user__pet__name__iregex=query) |
                Q(service__name__iregex=query) | Q(master__fam__iregex=query) |
                Q(master__name__iregex=query) | Q(master__otch__iregex=query))
            if date == "increasing":
                records = records.order_by("-date", "time")
            else:
                records = records.order_by("date", "time")
    return render(request, 'Salon/Administration.html', {'records': records})


def archive_admin(request):
    records = Record.objects.filter(status=3).order_by("-date", "time")
    context = {'records': records}
    return render(request, 'Salon/Archive_admin.html', context)


def create_groomer(request):
    form = CreateGroomer(request.POST)
    if request.method == 'POST':
        form = CreateGroomer(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'Salon/Groomer-ready.html')
    return render(request, 'Salon/Create-groomer.html', {'form': form})


def create_serv(request):
    form = CreateServ(request.POST)
    if request.method == 'POST':
        form = CreateServ(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'Salon/Serv-ready.html')
    return render(request, 'Salon/Create-serv.html', {'form': form})


def admin_status(request, rec_id):
    rec = Record.objects.get(id=rec_id)
    form = RecordChangeStatus
    if request.method == "POST":
        form = RecordChangeStatus(request.POST, instance=rec)
        if form.is_valid():
            form.save()
            return redirect('administration')
    return render(request, 'Salon/Admin-status.html', {'form': form})


def admin_services(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = CustomUser.objects.get(phone_number=request.user.phone_number)
    query = request.GET.get('search')
    if query is None:
        services = Service.objects.all()
    else:
        services = Service.objects.filter(Q(name__iregex=query) | Q(price__icontains=query) | Q(description__iregex=query))
    return render(request, 'Salon/Admin-services.html', {'services': services, 'user_profile': user_profile})


def change_service(request, serv_id):
    serv = Service.objects.get(id=serv_id)
    if request.method == 'POST':
        form = ChangeServ(request.POST, instance=serv)
        if form.is_valid():
            form.save()
            return redirect('admin_services')
    else:
        form = ChangeServ(instance=serv)
    return render(request, 'Salon/Change-serv-inf.html', {'form': form})


def admin_groomers(request):
    query = request.GET.get('search')
    if query is None:
        groomer = Employee.objects.all()
    else:
        groomer = Employee.objects.filter(
            Q(fam__iregex=query) | Q(name__iregex=query) | Q(otch__iregex=query))
    context = {'groomer': groomer}
    return render(request, 'Salon/Admin-groomers.html', context)


def change_groomer(request, groomer_id):
    groomer = Employee.objects.get(id=groomer_id)
    if request.method == 'POST':
        form = ChangeGroomer(request.POST, instance=groomer)
        if form.is_valid():
            form.save()
            return redirect('groomers')
    else:
        form = ChangeGroomer(instance=groomer)
    return render(request, 'Salon/Change-groomer-inf.html', {'form': form})


def admin_clients(request):
    query = request.GET.get('search')
    if query is None:
        clients = CustomUser.objects.all()
    else:
        clients = CustomUser.objects.filter(
            Q(phone_number__iregex=query) | Q(surname__iregex=query) | Q(name__iregex=query))
    context = {'clients': clients}
    return render(request, 'Salon/Admin-clients.html', context)


def admin_client_pets(request, client_id):
    client = CustomUser.objects.get(id=client_id)
    pets = PetAndUser.objects.filter(user=client)
    context = {'client': client, 'pets': pets}
    return render(request, 'Salon/Client-pets.html', context)


def admin_change_pet_inf(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    client_pet = PetAndUser.objects.get(pet=pet)
    client = CustomUser.objects.get(phone_number=client_pet.user.phone_number)
    if request.method == 'POST':
        form = PetChangeInf(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('admin_client_pets', client_id=client.id)
    else:
        form = PetChangeInf(instance=pet)
    return render(request, 'Salon/Change-pet-inf.html', {'form': form})


def admin_reg_pet(request, client_id):
    form = RegPetForm(request.POST)
    form.fields['race'].queryset = Race.objects.order_by("name_race")
    if request.method == 'POST':
        form = RegPetForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            race = form.cleaned_data['race']
            age = form.cleaned_data['age']
            photo = form.cleaned_data['photo']
            type = form.cleaned_data['type']
            pet = Pet.objects.create(
                name=name,
                race=race,
                age=age,
                type=type,
                photo=photo)
            user = CustomUser.objects.get(id=client_id)
            pet_user = PetAndUser.objects.create(pet=pet, user=user)
            pet_user.save()
            return redirect('admin_client_pets', client_id=client_id)
    return render(request, 'Salon/Reg-pet.html', {'form': form})


def admin_record(request, pet_id, client_id):
    form = RecordForm(request.POST)
    pet = Pet.objects.get(id=pet_id)
    form.fields['service'].queryset = Service.objects.filter(type=pet.type)
    client = CustomUser.objects.get(id=client_id)
    pet_user = PetAndUser.objects.get(pet=pet, user=client)
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.pet_user = pet_user
            rec.status = 1
            rec.save()
            return redirect('administration')
        else:
            return HttpResponse('Error')
    return render(request, 'Salon/Record.html', {'form': form, 'pet_user': pet_user})

# < Администрирование


def groomers(request):
    groomer = Employee.objects.all()
    context = {'groomer': groomer}
    return render(request, 'Salon/Groomers.html', context)

# Запись на прием >


def record(request, pet_id):
    form = RecordForm(request.POST)
    pet = Pet.objects.get(id=pet_id)
    form.fields['service'].queryset = Service.objects.filter(type=pet.type)
    pet_user = PetAndUser.objects.get(pet=pet, user=request.user)
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.pet_user = pet_user
            rec.status = 1
            rec.save()
            return render(request, 'Salon/Record-ready.html', {'form': form})
        else:
            return HttpResponse('Error')
    return render(request, 'Salon/Record.html', {'form': form, 'pet_user': pet_user})


def load_time(request):
    day = request.GET.get('date_id')
    master = request.GET.get('master_id')
    record_master = Record.objects.filter(master=master).filter(date=day).values_list('time', flat=True)
    available_times = []
    for time in CHOISE_TIME:
        if time not in record_master:
            available_times.append(time)
    return render(request, 'Salon/test.html', {'available_times': available_times})


def load_time_master(request):
    day = request.GET.get('date_id')
    master = request.GET.get('master_id')
    if day:
        record_master = Record.objects.filter(master=master).filter(date=day).values_list('time', flat=True)
    else:
        record_master = Record.objects.none().values_list('time', flat=True)
    available_times = []
    for time in CHOISE_TIME:
        if time not in record_master:
            available_times.append(time)
    return render(request, 'Salon/test.html', {'available_times': available_times})


# < Запись на прием


def change_pet_inf(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    if request.method == 'POST':
        form = PetChangeInf(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('lk')
    else:
        form = PetChangeInf(instance=pet)
    return render(request, 'Salon/Change-pet-inf.html', {'form': form})
