from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.producto_list, name='producto_list'),
]
