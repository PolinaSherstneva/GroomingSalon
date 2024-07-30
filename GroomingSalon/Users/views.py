from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin, messages
from Users.forms import CustomUserCreationForm, CustomUserChangeInf
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Users.models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'Users/signup.html'

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        print(self.request.user)
        # Через реквест передаем недостающую форму, которая обязательна
        fields.username = self.request.POST.get('phone_number')
        fields.fullname = f"{self.request.POST.get('surname')} {self.request.POST.get('name')}"
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # Сохраняем сообщение об ошибке в сессию
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)

        # Возвращаем HTTP-ответ с кодом ошибки
        return super().form_invalid(form)


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'Users/login.html'
    success_message = 'Успешная авторизация'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def form_invalid(self, form):
        # Сохраняем сообщение об ошибке в сессию
        messages.error(self.request, ('Ошибка аутентификации'))

        # Возвращаем HTTP-ответ с кодом ошибки
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('lk')


def change_username(request):
    if request.method == 'POST':
        form = CustomUserChangeInf(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('lk')
    else:
        form = CustomUserChangeInf(instance=request.user)
    return render(request, 'Users/change_username.html', {'form': form})


def change_username_id(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeInf(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_clients')
    else:
        form = CustomUserChangeInf(instance=user)
    return render(request, 'Users/change_username_id.html', {'form': form})





