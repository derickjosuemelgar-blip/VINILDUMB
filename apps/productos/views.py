from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Producto

from django.contrib.auth.decorators import user_passes_test
def es_admin(user):
    return user.is_authenticated and user.is_superuser

def lista_productos(request):
    productos = Producto.objects.all().order_by("nombre")

    return render(
        request,
        "lista.html",
        {"productos": productos},
    )

@user_passes_test (es_admin, login_url="/login/")
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

@user_passes_test(es_admin, login_url="/login/")
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, id=pk)

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

@user_passes_test (es_admin, login_url="/login/")
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, id=pk)

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