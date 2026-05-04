from decimal import Decimal
from django.conf import settings
from .models import Producto

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            # Inicializamos el carrito vacio en sesion
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                'producto_id': producto.id,
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'cantidad': 0,
                'imagen': producto.imagen_url if producto.imagen_url else (producto.imagen.url if producto.imagen else '')
            }
        self.carrito[producto_id]['cantidad'] += cantidad
        self.guardar_carrito()

    def restar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            self.carrito[producto_id]['cantidad'] -= 1
            if self.carrito[producto_id]['cantidad'] <= 0:
                self.eliminar(producto)
            else:
                self.guardar_carrito()

    def actualizar(self, producto, cantidad):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            if cantidad > 0:
                self.carrito[producto_id]['cantidad'] = cantidad
            else:
                self.eliminar(producto)
            self.guardar_carrito()

    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar_carrito()

    def guardar_carrito(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True

    def limpiar(self):
        self.session['carrito'] = {}
        self.session.modified = True

    def obtener_total(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())
        
    def __iter__(self):
        # Para que sea facil iterar en la plantilla, re-sacamos los valores como dicts, 
        # e inyectamos el total por item
        for item in self.carrito.values():
            item['total_item'] = Decimal(item['precio']) * item['cantidad']
            yield item

    def obtener_cantidad_total(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def __len__(self):
        # Devuelve el numero de productos diferentes en el carrito
        return len(self.carrito.keys())
