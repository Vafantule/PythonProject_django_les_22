from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']


def home_view(request):
    """
    Главная страница: отображение списка товаров.
    """
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {"products": products})


def contacts_view(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Вы получили новое сообщение от {name}({email}): {message}')
        success = True
    return render(request, 'catalog/contacts.html', {'success': success})


def product_detail_view(request, pk: int):
    """
    Контроллер для отображения страницы с подробной информацией о товаре.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


def add_product_view(request):
    """
    Страница с формой добавления нового товара.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProductForm()
    return render(request, "catalog/add_product.html", {"form": form})
