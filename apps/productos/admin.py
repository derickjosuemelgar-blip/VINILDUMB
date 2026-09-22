from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin (admin.ModelAdmin):
    list_display = ("nombre", "precio", "estilo")
    list_filter = ("estilo",)
    search_fields = ("nombre", "descripcion")
    
    

# Register your models here.
