from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from shop.models import Pedido

def home(request):
    from shop.models import Producto
    Producto.objects.filter(nombre__icontains='Saladito de lomo').delete()
    return render(request, 'core/index.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'core/register.html', {'nombre': nombre, 'email': email})
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Ya existe una cuenta con ese correo electrónico.')
            return render(request, 'core/register.html', {'nombre': nombre, 'email': email})
        
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = nombre
        user.save()
        login(request, user, backend='core.backends.EmailOrUsernameModelBackend')
        return redirect('home')
    return render(request, 'core/register.html')

@login_required
def mi_cuenta(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'core/mi_cuenta.html', {
        'pedidos': pedidos
    })

def contacto(request):
    if request.method == 'POST':
        messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Te responderemos lo antes posible.')
        return redirect('contacto')
    return render(request, 'core/contacto.html')
