from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to="products/")
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre