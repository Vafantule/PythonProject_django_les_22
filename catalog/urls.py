from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("add-product/", views.AddProductView.as_view(), name="add_product"),
    path("product/<int:pk>/update/", views.UpdateProductView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", views.DeleteProductView.as_view(), name="product_delete"),
]