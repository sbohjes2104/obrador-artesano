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
    path('admin-panel/pedido/eliminar/<int:pedido_id>/', views.eliminar_pedido_admin, name='eliminar_pedido_admin'),
    path('admin-panel/pedidos/eliminar-todos/', views.eliminar_todos_pedidos_admin, name='eliminar_todos_pedidos_admin'),
    path('admin-panel/producto/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('admin-panel/producto/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    
    # Checkout
    path('carrito/confirmar/', views.confirmar_reserva, name='confirmar_reserva'),
    path('pedido/<int:pedido_id>/confirmado/', views.pedido_confirmado, name='pedido_confirmado'),

    # API de Reseñas
    path('api/resenas/', views.api_reseñas, name='api_reseñas'),
    path('api/resenas/crear/', views.api_crear_reseña, name='api_crear_reseña'),
    path('api/resenas/responder/<int:resena_id>/', views.api_responder_resena, name='api_responder_resena'),
    path('api/resenas/eliminar/<int:resena_id>/', views.api_eliminar_resena, name='api_eliminar_resena'),
    path('api/resenas/respuesta/eliminar/<int:resena_id>/', views.api_eliminar_respuesta, name='api_eliminar_respuesta'),
]
