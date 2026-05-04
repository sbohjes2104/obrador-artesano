from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('productos/', views.producto_list, name='producto_list'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    
    # Carrito URLs
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/add/<int:producto_id>/', views.add_carrito, name='add_carrito'),
    path('carrito/restar/<int:producto_id>/', views.restar_carrito, name='restar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    
    # Admin Panel
    path('admin-panel/', views.administracion, name='administracion'),
    path('admin-panel/estado/<int:pedido_id>/', views.cambiar_estado_pedido, name='cambiar_estado'),
    
    # Checkout
    path('carrito/confirmar/', views.confirmar_reserva, name='confirmar_reserva'),
    path('pedido/<int:pedido_id>/confirmado/', views.pedido_confirmado, name='pedido_confirmado'),
]
