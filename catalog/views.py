from django.shortcuts import render


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
