from django.contrib import admin
from .models import Categoria, Producto, Alergeno, Pedido, LineaPedido


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unidad')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Alergeno)
class AlergenoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    list_filter = ('categoria', 'alergenos')
    search_fields = ('nombre',)
    filter_horizontal = ('alergenos',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'estado', 'total')
    list_filter = ('estado',)
    search_fields = ('usuario__username', 'usuario__email')
    list_editable = ('estado',)
    inlines = [LineaPedidoInline]


@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unidad')
