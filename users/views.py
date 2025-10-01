from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages


from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser
from typing import Any


class UserListView(ListView):
    """
    Список пользователей.
    """
    model = CustomUser
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetailView(DetailView):
    """
    Детали пользователя.
    """
    model = CustomUser
    template_name = "users/user_detail.html"
    context_object_name = "user"


class UserCreateView(CreateView):
    """
    Создание пользователя.
    """
    model = CustomUser
    fields = ["email", "username", "avatar", "phone", "country", "password",]
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")


class UserUpdateView(UpdateView):
    """
    Редактирование пользователя.
    """
    model = CustomUser
    fields = ["email", "username", "avatar", "phone", "country",]
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user_list")


class UserDeleteView(DeleteView):
    """
    Удаление пользователя.
    """
    model = CustomUser
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')


class UserRegistrationView(FormView):
    """
    Контроллер регистрации пользователя.
    """
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("user:user_login")

    def form_valid(self, form: UserRegistrationForm) -> Any:
        """
        Создание пользователя и отправление сообщений.
        """
        user = form.save()
        send_mail(
            subject="Добро пожаловать на сайт.",
            message="Спасибо за регистрацию на сайте!",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )
        return super().form_valid(form)


class UserLoginView(FormView):
    """
    Контроллер авторизации пользователя по email & password.
    """
    template_name = "user/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("catalog:index")

    def form_valid(self, form: UserLoginForm) -> Any:
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Неверные email или пароль.")
            return self.form_invalid(form)
