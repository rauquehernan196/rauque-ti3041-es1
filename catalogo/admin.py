from django.contrib import admin
from .models import PerfilUsuario, Carrito, ItemCarrito, Orden, ItemOrden

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'fecha_creacion')
    list_filter = ('rol', 'fecha_creacion')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('fecha_creacion',)

class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0
    readonly_fields = ('fecha_agregado',)

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_actualizacion', 'obtener_cantidad_items', 'obtener_total')
    search_fields = ('usuario__username',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    inlines = [ItemCarritoInline]

class ItemOrdenInline(admin.TabularInline):
    model = ItemOrden
    extra = 0
    readonly_fields = ('precio_unitario',)

class OrdenAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'usuario', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('numero_orden', 'usuario__username')
    readonly_fields = ('numero_orden', 'fecha_creacion')
    inlines = [ItemOrdenInline]

admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(Orden, OrdenAdmin)
