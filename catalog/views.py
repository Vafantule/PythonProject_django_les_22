from django.shortcuts import render
from .forms import ProductForm
from .models import Product, Category
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    """
    Главная страница: отображение списка товаров.
    """
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    """
    Контроллер отображения страницы с подробной информацией о товаре.
    """
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "pk"


class AddProductView(LoginRequiredMixin, CreateView):
    """
    Форма добавления нового товара.
    """
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateProductView(LoginRequiredMixin, UpdateView):
    """
    Контроллер обновления сведений о товаре.
    """
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"
    success_url = reverse_lazy("catalog:home")
    context_object_name = "product"
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteProductView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления товара.
    """
    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:home")
    context_object_name = "product"
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactsView(View):
    """
    Контроллер страницы контактов обработки формы.
    """
    def get(self, request):
        return render(request, "catalog/contacts.html", {"success": True})

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Вы получили новое сообщение от {name}({email}): {message}')
        return render(request, 'catalog/contacts.html', {'success': True})
