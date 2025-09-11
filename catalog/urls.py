from django.urls import path
from . import views
from .views import product_detail_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contacts/', views.contacts_view, name='contacts'),
    path("product/<int:pk>", views.product_detail_view, name="product_detail"),
]