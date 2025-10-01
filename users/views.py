from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import CustomUser


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
