import json
import os
from django.shortcuts import render
from django.http import Http404

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'datos.json')

def cargar_datos():
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)

def lista_productos(request):
    productos = cargar_datos()
    
    # Cálculos para el resumen de la Etapa 3
    total_registros = len(productos)
    disponibles = sum(1 for p in productos if p.get('stock', 0) > 0)

    context = {
        'productos': productos,
        'total_registros': total_registros,
        'disponibles': disponibles,
    }
    return render(request, 'catalogo/lista.html', context)

def detalle_producto(request, producto_id):
    productos = cargar_datos()
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if not producto:
        raise Http404("El producto no existe en el catálogo de ferretería.")
    return render(request, 'catalogo/detalle.html', {'producto': producto})