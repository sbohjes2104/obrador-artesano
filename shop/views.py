from django.shortcuts import render
from .models import Producto, Categoria

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
