from django.urls import path, include
from GroomingSalon import settings
from Users.views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/', SignUpView.as_view(), name='registrations'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Salon/Main.html'), name='logout'),
    path('changeinf/', change_username, name='changeinf'),
    path('changeinf_id/<int:user_id>', change_username_id, name='changeinf_id'),

]
