from django.shortcuts import render
from .models import Producto, Categoria

def producto_list(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'shop/producto_list.html', {
        'productos': productos,
        'categorias': categorias
    })
