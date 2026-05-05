from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Alergeno(models.Model):
    nombre = models.CharField(max_length=50)
    icono = models.CharField(max_length=100, help_text="Ruta de la imagen o clase CSS del icono", blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    descripcion = models.TextField(blank=True, default='')
    alergenos = models.ManyToManyField(Alergeno, blank=True, related_name='productos')

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PREPARANDO', 'Preparando'),
        ('LISTO', 'Listo para recoger'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dia_recogida = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre if self.producto else 'Producto eliminado'}"


class Reseña(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reseñas')
    texto = models.TextField()
    puntuacion = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)  # 0.5 a 5.0 estrellas
    fecha = models.DateTimeField(auto_now_add=True)
    respuesta = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Reseña de {self.usuario.first_name or self.usuario.username} ({self.puntuacion}★)"
