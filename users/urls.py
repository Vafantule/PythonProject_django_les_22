from django.urls import path
from .views import UserListView, UserDetailView, UserUpdateView, UserDeleteView, UserRegistrationView, UserLoginView
from django.contrib.auth.views import LogoutView

app_name = 'users'


urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path("<int:pk>", UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/edit/", UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),

    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("login/", UserLoginView.as_view(template_name="users/login.html"), name="user_login"),
    path("logout/", LogoutView.as_view(next_page='catalog:home'), name="user_logout"),
]
