import json
import os
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import PerfilUsuario, Carrito, ItemCarrito, Orden, ItemOrden
from .forms import LoginForm, RegistroForm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'datos.json')

def cargar_datos():
    """Carga los productos desde el archivo datos.json"""
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

def landing(request):
    """Vista de landing page principal"""
    if request.user.is_authenticated:
        return redirect('lista')
    return render(request, 'catalogo/landing.html')

def login_view(request):
    """Vista para el login"""
    if request.user.is_authenticated:
        return redirect('lista')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido {user.first_name}!")
                return redirect('lista')
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = LoginForm()
    
    return render(request, 'catalogo/login.html', {'form': form})

def register_view(request):
    """Vista para el registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('lista')
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Registro exitoso! Por favor inicia sesión.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistroForm()
    
    return render(request, 'catalogo/registro.html', {'form': form})

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('landing')

@login_required(login_url='login')
def lista_productos(request):
    """Vista del catálogo de productos"""
    productos = cargar_datos()
    
    total_registros = len(productos)
    disponibles = sum(1 for p in productos if p.get('stock', 0) > 0)
    
    usuario = request.user
    es_admin = False
    try:
        es_admin = usuario.perfil.es_admin()
    except PerfilUsuario.DoesNotExist:
        pass

    context = {
        'productos': productos,
        'total_registros': total_registros,
        'disponibles': disponibles,
        'es_admin': es_admin,
    }
    return render(request, 'catalogo/lista.html', context)

@login_required(login_url='login')
def detalle_producto(request, producto_id):
    """Vista del detalle de un producto"""
    productos = cargar_datos()
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if not producto:
        raise Http404("El producto no existe en el catálogo de ferretería.")
    
    usuario = request.user
    es_admin = False
    try:
        es_admin = usuario.perfil.es_admin()
    except PerfilUsuario.DoesNotExist:
        pass
    
    context = {
        'producto': producto,
        'es_admin': es_admin,
    }
    return render(request, 'catalogo/detalle.html', context)

@login_required(login_url='login')
def panel_admin(request):
    """Panel de administración para admin"""
    try:
        es_admin = request.user.perfil.es_admin()
    except PerfilUsuario.DoesNotExist:
        es_admin = False
    
    if not es_admin:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return redirect('lista')
    
    usuarios = User.objects.all()
    productos = cargar_datos()
    
    context = {
        'usuarios': usuarios,
        'productos': productos,
        'total_usuarios': usuarios.count(),
        'total_productos': len(productos),
    }
    return render(request, 'catalogo/panel_admin.html', context)

# ============================================================
# VISTAS DE CARRITO Y COMPRA
# ============================================================

@login_required(login_url='login')
@require_POST
def agregar_carrito(request, producto_id):
    """Agregar producto al carrito"""
    try:
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad < 1:
            cantidad = 1
    except ValueError:
        cantidad = 1
    
    productos = cargar_datos()
    producto = next((p for p in productos if p['id'] == producto_id), None)
    
    if not producto:
        messages.error(request, "El producto no existe.")
        return redirect('lista')
    
    if producto['stock'] < cantidad:
        messages.error(request, f"Solo hay {producto['stock']} unidades disponibles.")
        return redirect('lista')
    
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    
    try:
        item = ItemCarrito.objects.get(carrito=carrito, producto_id=producto_id)
        item.cantidad += cantidad
        if item.cantidad > producto['stock']:
            item.cantidad = producto['stock']
            messages.warning(request, f"Se alcanzó el máximo de stock disponible ({producto['stock']} unidades).")
        item.save()
        messages.success(request, "Cantidad actualizada en el carrito.")
    except ItemCarrito.DoesNotExist:
        ItemCarrito.objects.create(
            carrito=carrito,
            producto_id=producto_id,
            nombre_producto=producto['nombre'],
            precio=producto['precio'],
            cantidad=cantidad
        )
        messages.success(request, f"{producto['nombre']} agregado al carrito.")
    
    return redirect('ver_carrito')

@login_required(login_url='login')
def ver_carrito(request):
    """Ver el carrito de compras"""
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    
    productos = cargar_datos()
    items_con_disponibilidad = []
    hay_problema_stock = False
    
    for item in items:
        producto = next((p for p in productos if p['id'] == item.producto_id), None)
        stock_disponible = producto['stock'] if producto else 0
        hay_stock = stock_disponible >= item.cantidad
        
        if not hay_stock:
            hay_problema_stock = True
            
        items_con_disponibilidad.append({
            'item': item,
            'stock_disponible': stock_disponible,
            'hay_stock': hay_stock
        })
    
    context = {
        'carrito': carrito,
        'items_con_disponibilidad': items_con_disponibilidad,
        'hay_problema_stock': hay_problema_stock,
        'total': carrito.obtener_total(),
        'cantidad_items': carrito.obtener_cantidad_items(),
    }
    return render(request, 'catalogo/carrito.html', context)

@login_required(login_url='login')
@require_POST
def remover_carrito(request, item_id):
    """Remover item del carrito"""
    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        nombre = item.nombre_producto
        item.delete()
        messages.success(request, f"{nombre} removido del carrito.")
    except ItemCarrito.DoesNotExist:
        messages.error(request, "Item no encontrado en el carrito.")
    
    return redirect('ver_carrito')

@login_required(login_url='login')
@require_POST
def actualizar_cantidad(request, item_id):
    """Actualizar cantidad de un item en el carrito"""
    try:
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        if nueva_cantidad < 1:
            nueva_cantidad = 1
    except ValueError:
        messages.error(request, "Cantidad inválida.")
        return redirect('ver_carrito')
    
    try:
        item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user)
        productos = cargar_datos()
        producto = next((p for p in productos if p['id'] == item.producto_id), None)
        
        if not producto:
            messages.error(request, "Producto no encontrado.")
            return redirect('ver_carrito')
        
        if nueva_cantidad > producto['stock']:
            messages.error(request, f"Solo hay {producto['stock']} unidades disponibles.")
            return redirect('ver_carrito')
        
        item.cantidad = nueva_cantidad
        item.save()
        messages.success(request, "Cantidad actualizada.")
    except ItemCarrito.DoesNotExist:
        messages.error(request, "Item no encontrado en el carrito.")
    
    return redirect('ver_carrito')

@login_required(login_url='login')
def procesar_compra(request):
    """Procesar la compra y crear una orden"""
    carrito = Carrito.objects.get(usuario=request.user)
    items = carrito.items.all()
    
    if not items.exists():
        messages.error(request, "El carrito está vacío.")
        return redirect('ver_carrito')
    
    productos = cargar_datos()
    
    for item in items:
        producto = next((p for p in productos if p['id'] == item.producto_id), None)
        if not producto or producto['stock'] < item.cantidad:
            stock_disp = producto['stock'] if producto else 0
            messages.error(
                request, 
                f"No hay suficiente stock de '{item.nombre_producto}'. "
                f"Disponible: {stock_disp}, Solicitado: {item.cantidad}"
            )
            return redirect('ver_carrito')
    
    numero_orden = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{request.user.id}"
    total = carrito.obtener_total()
    cantidad_items = sum(item.cantidad for item in items)
    
    orden = Orden.objects.create(
        usuario=request.user,
        numero_orden=numero_orden,
        total=total,
        cantidad_items=cantidad_items,
        estado='completada'
    )
    
    for item in items:
        ItemOrden.objects.create(
            orden=orden,
            producto_id=item.producto_id,
            nombre_producto=item.nombre_producto,
            precio_unitario=item.precio,
            cantidad=item.cantidad
        )
    
    actualizar_stock_json(productos, items)
    carrito.items.all().delete()
    
    messages.success(request, f"¡Compra realizada! Orden: {numero_orden}")
    return redirect('compra_exitosa', orden_id=orden.id)

@login_required(login_url='login')
def compra_exitosa(request, orden_id):
    """Vista de confirmación de compra"""
    try:
        orden = Orden.objects.get(id=orden_id, usuario=request.user)
    except Orden.DoesNotExist:
        messages.error(request, "Orden no encontrada.")
        return redirect('lista')
    
    items = orden.items.all()
    
    context = {
        'orden': orden,
        'items': items,
        'total': orden.total,
    }
    return render(request, 'catalogo/compra_exitosa.html', context)

@login_required(login_url='login')
def mis_ordenes(request):
    """Ver todas las órdenes del usuario"""
    ordenes = Orden.objects.filter(usuario=request.user)
    
    context = {
        'ordenes': ordenes,
    }
    return render(request, 'catalogo/mis_ordenes.html', context)

def actualizar_stock_json(productos, items_comprados):
    """Actualiza el stock en el archivo JSON después de una compra."""
    compras = {item.producto_id: item.cantidad for item in items_comprados}
    
    for producto in productos:
        if producto['id'] in compras:
            producto['stock'] -= compras[producto['id']]
            if producto['stock'] < 0:
                producto['stock'] = 0
    
    try:
        with open(JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(productos, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error al actualizar JSON: {e}")