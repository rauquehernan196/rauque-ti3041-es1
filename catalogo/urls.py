from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Catálogo
    path('catalogo/', views.lista_productos, name='lista'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle'),
    
    # Carrito y compra
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/remover/<int:item_id>/', views.remover_carrito, name='remover_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/procesar/', views.procesar_compra, name='procesar_compra'),
    path('compra-exitosa/<int:orden_id>/', views.compra_exitosa, name='compra_exitosa'),
    path('mis-ordenes/', views.mis_ordenes, name='mis_ordenes'),
    
    # Admin personalizado (Actualizado a 'panel/' para evitar conflicto con admin/)
    path('panel/', views.panel_admin, name='panel_admin'),
]