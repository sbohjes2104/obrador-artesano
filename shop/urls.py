from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('productos/', views.producto_list, name='producto_list'),
]
