from django.urls import path

from . import views


app_name = "carrito"


urlpatterns = [
    path("", views.ver_carrito, name="ver"),
    path("agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar"),
    path("actualizar/<int:id>/", views.actualizar_carrito, name="actualizar"),
    path("eliminar/<int:id>/", views.eliminar_del_carrito, name="eliminar"),
    path('checkout/', views.checkout, name='checkout'),          
               
]