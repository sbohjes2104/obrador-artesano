from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Producto, Categoria, Alergeno, Pedido, LineaPedido
from .cart import Carrito

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
        
        # Vaciar el carrito
        carrito.limpiar()
        
        messages.success(request, f'¡Pedido #{pedido.id} confirmado! Te esperamos en la tienda para la recogida. 🍞')
        return redirect('shop:pedido_confirmado', pedido_id=pedido.id)
    
    return redirect('shop:ver_carrito')


@login_required
def pedido_confirmado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'shop/pedido_confirmado.html', {'pedido': pedido})


@staff_member_required
def administracion(request):
    # Todos los pedidos
    pedidos = Pedido.objects.all().order_by('-fecha')
    
    # Resumen de Producción: sumar cantidades de productos en estados PENDIENTE o PREPARANDO
    pedidos_pendientes = Pedido.objects.filter(estado__in=['PENDIENTE', 'PREPARANDO'])
    produccion = {}
    
    for pedido in pedidos_pendientes:
        for linea in pedido.lineas.all():
            nombre = linea.producto.nombre if linea.producto else "Producto eliminado"
            if nombre in produccion:
                produccion[nombre] += linea.cantidad
            else:
                produccion[nombre] = linea.cantidad
                
    # Armar string de resumen "Total para hoy: 1 Pan integral, 2 Pan de centeno..."
    resumen_lista = [f"{cantidad} {nombre}" for nombre, cantidad in produccion.items()]
    resumen_texto = ", ".join(resumen_lista) if resumen_lista else "No hay producción pendiente"
    resumen_texto = f"Total para hoy: {resumen_texto}"
    
    estados = Pedido.ESTADOS
    
    return render(request, 'shop/administracion.html', {
        'pedidos': pedidos,
        'resumen_texto': resumen_texto,
        'estados': estados
    })

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
