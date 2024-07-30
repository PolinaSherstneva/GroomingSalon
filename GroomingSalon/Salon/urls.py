from django.urls import path
from . import views
from Users import views as user_views


urlpatterns = [
    path('', views.main, name="home"),
    path('services', views.services, name="services"),
    path('lk', views.lk, name="lk"),
    path('archive_lk', views.archive_lk, name="archive_lk"),
    path('portfolio/<int:master_id>', views.portfolio, name="portfolio"),
    path('groomers', views.groomers, name="groomers"),
    path('administration', views.administration, name="administration"),
    path('archive_admin', views.archive_admin, name="archive_admin"),
    path('create-groomer', views.create_groomer, name="create_groomer"),
    path('create-serv', views.create_serv, name="create_serv"),
    path('record/<int:pet_id>', views.record, name="record"),
    path('reg-pet', views.reg_pet, name="reg-pet"),
    path('admin_status/<int:rec_id>', views.admin_status, name="admin_status"),
    path('admin-groomers', views.admin_groomers, name="admin_groomers"),
    path('admin-services', views.admin_services, name="admin_services"),
    path('admin-clients', views.admin_clients, name="admin_clients"),
    path('admin-client-pets/<int:client_id>', views.admin_client_pets, name="admin_client_pets"),
    path('admin-change-pet-inf/<int:pet_id>', views.admin_change_pet_inf, name="admin_change_pet_inf"),
    path('admin-reg-pet/<int:client_id>', views.admin_reg_pet, name="admin_reg_pet"),
    path('admin-record/<int:pet_id>/<int:client_id>', views.admin_record, name="admin_record"),
    path('change-pet-inf/<int:pet_id>', views.change_pet_inf, name="change-pet-inf"),
    path('change-service/<int:serv_id>', views.change_service, name="change-service"),
    path('change-groomer/<int:groomer_id>', views.change_groomer, name="change-groomer"),
    path('ajax/load-time/', views.load_time, name='ajax-load-time'),
    path('ajax/load-time-master/', views.load_time_master, name='ajax-load-time-master'),
    path('ajax/load-race/', views.load_race, name='ajax-load-race'),
]
