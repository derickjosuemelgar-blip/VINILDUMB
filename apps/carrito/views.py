from decimal import Decimal
from math import prod

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.productos.models import Producto
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pedido


def obtener_carrito(request):
    return request.session.get("carrito", {})


def guardar_carrito(request, carrito):
    request.session["carrito"] = carrito
    request.session.modified = True


def ver_carrito(request):
    carrito = obtener_carrito(request)

    productos_carrito = []
    total = Decimal("0.00")

    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.filter(id=producto_id).first()

        if producto is None:
            continue

        subtotal = producto.precio * cantidad

        productos_carrito.append(
            {
                "producto": producto,
                "cantidad": cantidad,
                "subtotal": subtotal,
            }
        )

        total += subtotal

    return render(
        request,
        "carrito.html",
        {
            "productos_carrito": productos_carrito,
            "total": total,
        },
    )

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        
        if producto_id_str in carrito:
            carrito[producto_id_str] += cantidad
        else:
            carrito[producto_id_str] = cantidad

        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('productos:lista')

    carrito[str(producto.id)] = nueva_cantidad
    guardar_carrito(request, carrito)

    messages.success(
        request,
        "Producto agregado al carrito.",
    )

    return redirect("productos:lista")

def actualizar_carrito(request, id):
    if request.method != "POST":
        return redirect("carrito:ver")

    producto = get_object_or_404(Producto, id=id)

    try:
        cantidad = int(request.POST.get("cantidad", 0))
    except (TypeError, ValueError):
        cantidad = 0

    if cantidad < 1:
        messages.error(
            request,
            "La cantidad debe ser como mínimo 1.",
        )
        return redirect("carrito:ver")

    if cantidad > producto.cantidad_disponible:
        messages.error(
            request,
            "La cantidad solicitada supera el inventario disponible.",
        )
        return redirect("carrito:ver")

    carrito = obtener_carrito(request)

    if str(producto.id) not in carrito:
        messages.error(
            request,
            "El producto no se encuentra en el carrito.",
        )
        return redirect("carrito:ver")

    carrito[str(producto.id)] = cantidad
    guardar_carrito(request, carrito)

    messages.success(
        request,
        "Cantidad actualizada.",
    )

    return redirect("carrito:ver")


def eliminar_del_carrito(request, id):
    if request.method != "POST":
        return redirect("carrito:ver_carrito")

    carrito = obtener_carrito(request)
    producto_id = str(id)

    if producto_id in carrito:
        del carrito[producto_id]
        guardar_carrito(request, carrito)
        messages.success(
            request,
            "Producto eliminado del carrito.",
        )

    return redirect("carrito:ver")

def checkout(request):
    carrito = obtener_carrito(request)

    productos_carrito = []
    total = Decimal("0.00")

    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.filter(id=producto_id).first()

        if producto is None:
            continue

        subtotal = producto.precio * cantidad

        productos_carrito.append({
            "producto": producto,
            "cantidad": cantidad,
            "subtotal": subtotal,
        })

        total += subtotal

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellidos = request.POST.get("apellidos")
        nit = request.POST.get("nit")
        direccion = request.POST.get("direccion")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")
        departamento = request.POST.get("departamento")
        municipio = request.POST.get("municipio")
        metodo_pago = request.POST.get("metodo_pago") or request.POST.get("pago")

        campos_obligatorios = [nombre, apellidos, nit, direccion, telefono, correo]
        if not all(campos_obligatorios):
            messages.error(request, "Debe rellenar todos los campos obligatorios.")
            return render(
                request,
                "checkout.html",
                {
                    "productos_carrito": productos_carrito,
                    "total": total,
                },
            )

        for item in productos_carrito:
            producto = item["producto"]
            cantidad = item["cantidad"]

            if cantidad > producto.cantidad_disponible:
                messages.error(
                    request,
                    f"No hay suficiente stock de {producto.nombre}.",
                )
                return redirect("carrito:ver")
            
        nuevo_pedido = Pedido.objects.create(
            nombre=nombre,
            apellidos=apellidos,
            nit=nit,
            direccion=direccion,
            telefono=telefono,
            correo=correo,
            departamento=departamento,
            municipio=municipio,
            metodo_pago=metodo_pago,
            total=total
        )
        
        for item in productos_carrito:
            producto = item["producto"]
            cantidad = item["cantidad"]

            producto.cantidad_disponible -= cantidad
            producto.save(update_fields=["cantidad_disponible"])
            

        request.session["carrito"] = {}
        request.session.modified = True
        
        return render(
            request,
            "confirmacion.html",
            {
                "pedido": nuevo_pedido,
                "total": total,
                "metodo_pago": metodo_pago,
            }
        )

    return render(
        request,
        "checkout.html",
        {
            "productos_carrito": productos_carrito,
            "total": total,
        },
    )