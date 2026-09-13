from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto


def lista_productos(request):
    productos = Producto.objects.all().order_by("nombre")

    return render(
        request,
        "lista.html",
        {"productos": productos},
    )


def crear_producto(request):
    if request.method == "POST":
        formulario = ProductoForm(
            request.POST,
            request.FILES,
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(
                request,
                "Producto creado correctamente.",
            )
            return redirect("productos:lista")
    else:
        formulario = ProductoForm()

    return render(
        request,
        "formulario.html",
        {
            "formulario": formulario,
            "titulo": "Crear producto",
        },
    )


def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        formulario = ProductoForm(
            request.POST,
            request.FILES,
            instance=producto,
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(
                request,
                "Producto actualizado correctamente.",
            )
            return redirect("productos:lista")
    else:
        formulario = ProductoForm(instance=producto)

    return render(
        request,
        "formulario.html",
        {
            "formulario": formulario,
            "titulo": "Editar producto",
            "producto": producto,
        },
    )


def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.delete()
        messages.success(
            request,
            "Producto eliminado correctamente.",
        )
        return redirect("productos:lista")

    return render(
        request,
        "confirmar_eliminacion.html",
        {"producto": producto},
    )