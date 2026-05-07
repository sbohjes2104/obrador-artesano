from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Producto, Categoria, Alergeno, Pedido, LineaPedido, Reseña
from .cart import Carrito
from .forms import ProductoForm
from django.utils import timezone


def producto_list(request):
    category_name = request.GET.get('category')
    categorias = Categoria.objects.all()
    
    if category_name:
        productos = Producto.objects.filter(categoria__nombre__iexact=category_name)
        grouped_products = None
    else:
        # Group products by category
        grouped_products = []
        for cat in categorias:
            productos_cat = Producto.objects.filter(categoria=cat)
            if productos_cat.exists():
                grouped_products.append({
                    'categoria': cat,
                    'productos': productos_cat
                })
        productos = None
        
    return render(request, 'shop/producto_list.html', {
        'productos': productos,
        'grouped_products': grouped_products,
        'categorias': categorias,
        'category_selected': category_name
    })

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'shop/producto_detalle.html', {
        'producto': producto
    })

def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'shop/carrito.html', {
        'carrito': carrito
    })

def add_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except ValueError:
        cantidad = 1
        
    if cantidad > producto.stock:
        messages.error(request, f'Lo sentimos, solo quedan {producto.stock} unidades de {producto.nombre}.')
        return redirect('shop:producto_detalle', producto_id=producto_id)
        
    carrito.agregar(producto=producto, cantidad=cantidad)
    messages.success(request, f'✓ {producto.nombre} añadido al carrito')
    return redirect('shop:producto_detalle', producto_id=producto_id)

def restar_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.restar(producto=producto)
    return redirect('shop:ver_carrito')

def eliminar_carrito(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto=producto)
    return redirect('shop:ver_carrito')


@login_required
def confirmar_reserva(request):
    if request.method == 'POST':
        carrito = Carrito(request)
        
        if len(carrito) == 0:
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('shop:ver_carrito')
        
        # Crear el pedido en la BD
        pedido = Pedido.objects.create(
            usuario=request.user,
            total=carrito.obtener_total(),
            estado='PENDIENTE',
            dia_recogida=request.POST.get('pickup_day')
        )
        
        # Crear cada línea del pedido
        for item in carrito:
            producto = get_object_or_404(Producto, id=item['producto_id'])
            LineaPedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unidad=item['precio']
            )
            # Descontar stock
            producto.stock -= item['cantidad']
            producto.save()
        
        # Vaciar el carrito
        carrito.limpiar()

        return redirect('shop:pedido_confirmado', pedido_id=pedido.id)
    
    return redirect('shop:ver_carrito')


@login_required
def pedido_confirmado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'shop/pedido_confirmado.html', {'pedido': pedido})


@staff_member_required
def administracion(request):
    # Formulario para nuevo producto
    if request.method == 'POST' and 'crear_producto' in request.POST:
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto creado con éxito!')
            return redirect('shop:administracion')
    else:
        form = ProductoForm()

    # Todos los pedidos
    pedidos = Pedido.objects.all().order_by('-fecha')
    
    # Resumen de Producción por días
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    produccion_por_dia = {dia: {} for dia in dias_semana}
    
    pedidos_pendientes = Pedido.objects.filter(estado__in=['PENDIENTE', 'PREPARANDO']).prefetch_related('lineas__producto')
    
    for pedido in pedidos_pendientes:
        dia_str = pedido.dia_recogida or "Hoy"
        # Normalizar día
        if "Lunes" in dia_str: dia_key = "Lunes"
        elif "Martes" in dia_str: dia_key = "Martes"
        elif "Miércoles" in dia_str: dia_key = "Miércoles"
        elif "Jueves" in dia_str: dia_key = "Jueves"
        elif "Viernes" in dia_str: dia_key = "Viernes"
        elif "Sábado" in dia_str: dia_key = "Sábado"
        elif "Domingo" in dia_str: dia_key = "Domingo"
        else:
            # Si es "Hoy" o algo no reconocido, usar el día actual
            hoy_idx = timezone.now().weekday() # 0 es Lunes
            dia_key = dias_semana[hoy_idx]
            
        for linea in pedido.lineas.all():
            nombre = linea.producto.nombre if linea.producto else "Producto eliminado"
            if nombre in produccion_por_dia[dia_key]:
                produccion_por_dia[dia_key][nombre] += linea.cantidad
            else:
                produccion_por_dia[dia_key][nombre] = linea.cantidad
                
    hoy_idx = timezone.now().weekday()
    dia_actual = dias_semana[hoy_idx]
                
    resumen_lineas = []
    for dia in dias_semana:
        if produccion_por_dia[dia]:
            label = f"Hoy ({dia})" if dia == dia_actual else dia
            items = [f"{cant} {nom}" for nom, cant in produccion_por_dia[dia].items()]
            resumen_lineas.append(f"<strong>{label}:</strong> " + ", ".join(items))
            
    resumen_texto = "<br>".join(resumen_lineas) if resumen_lineas else "No hay producción pendiente"

    
    estados = Pedido.ESTADOS
    
    return render(request, 'shop/administracion.html', {
        'pedidos': pedidos,
        'resumen_texto': resumen_texto,
        'estados': estados,
        'form': form,
        'productos': Producto.objects.all().order_by('categoria', 'nombre')
    })

@staff_member_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('shop:administracion')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'shop/editar_producto.html', {'form': form, 'producto': producto})

@staff_member_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado del catálogo.')
    return redirect('shop:administracion')

@staff_member_required
def cambiar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nuevo_estado = request.POST.get('estado')
        
        # Validar que sea un estado permitido
        estados_validos = [e[0] for e in Pedido.ESTADOS]
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            pedido.save()
            
    return redirect('shop:administracion')


@require_POST
def eliminar_pedido_admin(request, pedido_id):
    if request.user.is_staff:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.delete()
        messages.success(request, f'Pedido #{pedido.id} eliminado del historial.')
    return redirect('shop:administracion')


@require_POST
def eliminar_todos_pedidos_admin(request):
    if request.user.is_staff:
        Pedido.objects.all().delete()
        messages.success(request, 'Todo el historial de pedidos ha sido eliminado.')
    return redirect('shop:administracion')


# ─────────────────────────────────────────────
#  API DE RESEÑAS
# ─────────────────────────────────────────────

@require_GET
def api_reseñas(request):
    """GET /api/reseñas/ → devuelve todas las reseñas en formato JSON."""
    reseñas = Reseña.objects.select_related('usuario').all()
    data = []
    for r in reseñas:
        data.append({
            'id': r.id,
            'usuario': r.usuario.first_name or r.usuario.username,
            'usuario_id': r.usuario.id,
            'texto': r.texto,
            'puntuacion': float(r.puntuacion),
            'fecha': r.fecha.strftime('%d/%m/%Y'),
            'respuesta': r.respuesta,
            'fecha_respuesta': r.fecha_respuesta.strftime('%d/%m/%Y') if r.fecha_respuesta else None,
        })
    return JsonResponse({'resenas': data})


@csrf_exempt
@require_POST
def api_crear_reseña(request):
    """POST /api/reseñas/crear/ → crea una reseña, responde JSON."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Debes iniciar sesión para dejar una reseña.'}, status=401)

    try:
        body = json.loads(request.body)
        texto = body.get('texto', '').strip()
        puntuacion = float(body.get('puntuacion', 5.0))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

    if not texto:
        return JsonResponse({'error': 'El comentario no puede estar vacío.'}, status=400)
    if not (0.5 <= puntuacion <= 5.0):
        return JsonResponse({'error': 'La puntuación debe estar entre 0.5 y 5.'}, status=400)

    reseña = Reseña.objects.create(
        usuario=request.user,
        texto=texto,
        puntuacion=puntuacion,
    )

    return JsonResponse({
        'status': 'ok',
        'resena': {
            'id': reseña.id,
            'usuario': reseña.usuario.first_name or reseña.usuario.username,
            'usuario_id': reseña.usuario.id,
            'texto': reseña.texto,
            'puntuacion': reseña.puntuacion,
            'fecha': reseña.fecha.strftime('%d/%m/%Y'),
            'respuesta': None,
        }
    }, status=201)

from django.utils import timezone

@csrf_exempt
@require_POST
def api_responder_resena(request, resena_id):
    """POST /api/resenas/responder/<id>/ → permite al superuser responder."""
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({'error': 'Solo el administrador puede responder.'}, status=403)

    try:
        body = json.loads(request.body)
        respuesta = body.get('respuesta', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

    if not respuesta:
        return JsonResponse({'error': 'La respuesta no puede estar vacía.'}, status=400)

    try:
        reseña = Reseña.objects.get(id=resena_id)
        reseña.respuesta = respuesta
        reseña.fecha_respuesta = timezone.now()
        reseña.save()
    except Reseña.DoesNotExist:
        return JsonResponse({'error': 'Reseña no encontrada.'}, status=404)

    return JsonResponse({
        'status': 'ok',
        'fecha_respuesta': reseña.fecha_respuesta.strftime('%d/%m/%Y')
    })

@csrf_exempt
def api_eliminar_resena(request, resena_id):
    """DELETE /api/resenas/eliminar/<id>/ → autor o admin."""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Inicia sesión para realizar esta acción.'}, status=401)

    try:
        reseña = Reseña.objects.get(id=resena_id)
        # Comprobar si es el autor o es superuser
        if reseña.usuario != request.user and not request.user.is_superuser:
            return JsonResponse({'error': 'No tienes permiso para eliminar esta reseña.'}, status=403)
        
        reseña.delete()
        return JsonResponse({'status': 'ok'})
    except Reseña.DoesNotExist:
        return JsonResponse({'error': 'Reseña no encontrada.'}, status=404)

@csrf_exempt
def api_eliminar_respuesta(request, resena_id):
    """DELETE /api/resenas/respuesta/eliminar/<id>/ → solo admin."""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse({'error': 'No tienes permiso para eliminar respuestas.'}, status=403)

    try:
        reseña = Reseña.objects.get(id=resena_id)
        reseña.respuesta = None
        reseña.fecha_respuesta = None
        reseña.save()
        return JsonResponse({'status': 'ok'})
    except Reseña.DoesNotExist:
        return JsonResponse({'error': 'Reseña no encontrada.'}, status=404)
