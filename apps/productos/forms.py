from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "precio",
            "cantidad_disponible",
            "imagen",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del vino",
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "cantidad_disponible": forms.NumberInput(
                attrs={
                    "min": "0",
                }
            ),
        }