from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
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

@login_required
def editar_pedido_cuenta(request, pedido_id):
    from django.shortcuts import get_object_or_404
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    if pedido.estado != 'PENDIENTE':
        messages.error(request, 'Solo puedes editar pedidos en estado Pendiente.')
        return redirect('mi_cuenta')
        
    if request.method == 'POST':
        nuevo_dia = request.POST.get('dia_recogida')
        if nuevo_dia:
            pedido.dia_recogida = nuevo_dia
            pedido.save()
            messages.success(request, f'Pedido #{pedido.id:03d} actualizado correctamente.')
            return redirect('mi_cuenta')
            
    return render(request, 'core/editar_pedido_cuenta.html', {'pedido': pedido})

@login_required
@require_POST
def cancelar_pedido_cuenta(request, pedido_id):
    from django.shortcuts import get_object_or_404
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    if pedido.estado != 'PENDIENTE':
        messages.error(request, 'Solo puedes cancelar pedidos en estado Pendiente.')
        return redirect('mi_cuenta')
        
    # Restaurar el stock
    for linea in pedido.lineas.all():
        if linea.producto:
            linea.producto.stock += linea.cantidad
            linea.producto.save()
            
    # Eliminar pedido
    pedido_id_str = f"#{pedido.id:03d}"
    pedido.delete()
    messages.success(request, f'El pedido {pedido_id_str} ha sido cancelado con éxito.')
    
    return redirect('mi_cuenta')

def contacto(request):
    if request.method == 'POST':
        import time
        # Cooldown: Evitar spam (60 segundos entre envíos)
        ahora = int(time.time())
        ultimo_envio = request.session.get('contacto_last_submit', 0)
        
        if ahora - ultimo_envio < 60:
            segundos_restantes = 60 - (ahora - ultimo_envio)
            messages.error(request, f'Por favor, espera {segundos_restantes} segundos antes de enviar otro mensaje.')
            return redirect('contacto')

        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        cuerpo = f"Nombre: {nombre}\nCorreo: {email}\nAsunto: {asunto}\n\nMensaje:\n{mensaje}"
        
        try:
            send_mail(
                subject=f"Nuevo mensaje de contacto: {asunto}",
                message=cuerpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            # Actualizar el tiempo del último envío
            request.session['contacto_last_submit'] = ahora
            messages.success(request, '¡Tu mensaje ha sido enviado correctamente! Te responderemos lo antes posible.')
        except Exception:
            messages.error(request, 'Hubo un error al enviar tu mensaje. Por favor, inténtalo de nuevo más tarde.')
            
        return redirect('contacto')
    return render(request, 'core/contacto.html')
