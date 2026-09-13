from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellidos', 'nit', 'total', 'fecha_creacion')
    search_fields = ('nombre', 'apellidos', 'nit', 'correo')
    list_filter = ('departamento', 'fecha_creacion')