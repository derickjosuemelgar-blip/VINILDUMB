from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to="products/", blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    estilo = models.CharField(max_length=50, default= "rock")
    audio_preview = models.FileField(upload_to="previews/", blank=True, null= True)
    imagen_izquierda = models.ImageField(upload_to='modales/', blank=True, null=True)
    imagen_derecha = models.ImageField(upload_to='modales/', blank=True, null=True)

    def __str__(self):
        return self.nombre