from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin, UserPassesTestMixin)
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from django_les_22.settings import CACHE_ENABLED
from .forms import ProductForm
from .models import Category, Product
from .services import get_products_by_category


class HomeView(ListView):
    """
    Главная страница: отображение списка товаров.
    Добавлено низкоуровневое кеширование (Redis).
    """
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """
        Получение и кеширование списка продуктов.
        """
        if CACHE_ENABLED:
            products = cache.get("products_list")
            if products is None:
                products = Product.objects.all()
                cache.set("products_list", products, 60 * 10)
        else:
            products = Product.objects.all()
        return products


class ProductDetailView(DetailView):
    """
    Контроллер отображения страницы с подробной информацией о товаре.
    """
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_moderator'] = (user.is_authenticated and user.groups.filter(name="Модератор продуктов").exists())
        return context

    @method_decorator(cache_page(60 * 15))
    def dispatch(self, request, *args, **kwargs):
        """
        Кеширует страницу продукта.
        """
        return super().dispatch(request, *args, **kwargs)


class AddProductView(LoginRequiredMixin, CreateView):
    """
    Форма добавления нового товара.
    """
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"

    def form_valid(self, form: ProductForm) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class UpdateProductView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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

    def get_success_url(self) -> str:
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def test_func(self) -> bool:
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        return HttpResponseForbidden("Редактировать продукт может только владелец.")


class DeleteProductView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Контроллер удаления товара.
    """
    model = Product
    template_name = "catalog/product_delete.html"
    context_object_name = "product"
    pk_url_kwarg = "pk"
    permission_required = "catalog.delete_product"
    login_url = "users:user_login"

    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super().delete(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse("catalog:home")

    def test_func(self) -> bool:
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.group.filter(name="Модератор продуктов").exists()

    def handle_no_permission(self):
        return HttpResponseForbidden("Удалять продукт может только владелец или модератор.")


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


class CategoryProductListView(ListView):
    """
    Представление отображения продуктов в заданной категории.
    """
    template_name = "catalog/products_by_category.html"
    context_object_name = "products"

    def get_queryset(self) -> Any:
        """
        Получение продуктов по категориям.
        """
        category_id = self.kwargs.get("category_id")
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs) -> dict:
        """
        Добавление объекта категории в контекст.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, id=category_id)
        context["category"] = category
        return context


class CategoryListView(ListView):
    """
    Отображение списка категорий.
    """
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = "categories"
