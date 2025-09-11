from django.shortcuts import render, get_object_or_404
from .models import Product


def home_view(request):
    return render(request, 'catalog/home.html')


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
