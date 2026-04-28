from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def home(request):
    return render(request, 'core/index.html')

def register(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password == password_confirm:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = nombre
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'core/register.html')
