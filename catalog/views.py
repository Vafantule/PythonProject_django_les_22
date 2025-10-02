from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import ProductForm
from .models import Category, Product


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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class UpdateProductView(LoginRequiredMixin, UpdateView):
    """
    Контроллер обновления сведений о товаре.
    """
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"
    context_object_name = "product"
    pk_url_kwarg = "pk"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class DeleteProductView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Контроллер удаления товара.
    """
    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:home")
    context_object_name = "product"
    pk_url_kwarg = "pk"
    permission_required = "catalog.delete_product"
    login_url = "users:user_login"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().delete(request, *args, **kwargs)


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


class ProductUnpublishView(PermissionRequiredMixin, UpdateView):
    """
    Отмена публикации продукта, только пользователям с правами can_unpublish_product.
    """
    model = Product
    fields = []
    permission_required = "catalog.can_unpublish_product"
    template_name = "catalog/product_unpublish_confirm.html"
    login_url = "users:user_login"

    def form_valid(self, form):
        if self.object.status == "published":
            self.object.status = "unpublished"
            self.object.save()
            messages.success(self.request, "Товар успешно снят с публикации.")
        else:
            messages.warning(self.request, "Товар не опубликован, действие невозможно.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})
