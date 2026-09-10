from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    ROLES = (
        ('usuario', 'Usuario Normal'),
        ('admin', 'Administrador'),
    )
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
    
    def es_admin(self):
        return self.rol == 'admin'
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"


class Carrito(models.Model):
    """Carrito de compras del usuario"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    def obtener_total(self):
        """Calcula el total del carrito"""
        return sum(item.obtener_subtotal() for item in self.items.all())
    
    def obtener_cantidad_items(self):
        """Retorna la cantidad total de items en el carrito"""
        return sum(item.cantidad for item in self.items.all())
    
    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"


class ItemCarrito(models.Model):
    """Item individual en el carrito"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto_id = models.IntegerField()  # ID del producto en JSON
    nombre_producto = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre_producto} x{self.cantidad}"
    
    def obtener_subtotal(self):
        """Calcula el subtotal del item"""
        return self.precio * self.cantidad
    
    class Meta:
        verbose_name = "Item Carrito"
        verbose_name_plural = "Items Carrito"
        unique_together = ('carrito', 'producto_id')  # Un producto una sola vez por carrito


class Orden(models.Model):
    """Registro de compras completadas"""
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordenes')
    numero_orden = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='completada')
    total = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad_items = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Orden {self.numero_orden} - {self.usuario.username}"
    
    class Meta:
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        ordering = ['-fecha_creacion']


class ItemOrden(models.Model):
    """Items de una orden completada"""
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto_id = models.IntegerField()
    nombre_producto = models.CharField(max_length=255)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.nombre_producto} x{self.cantidad}"
    
    def obtener_subtotal(self):
        return self.precio_unitario * self.cantidad
    
    class Meta:
        verbose_name = "Item Orden"
        verbose_name_plural = "Items Orden"


# ============================================================
# SIGNALS - Sincronizar rol admin con permisos de Django
# ============================================================

@receiver(post_save, sender=PerfilUsuario)
def sincronizar_permisos_admin(sender, instance, created, **kwargs):
    """
    Cuando el rol cambia a 'admin', automáticamente se actualizan
    los permisos de Django (is_staff, is_superuser)
    """
    usuario = instance.usuario
    
    if instance.rol == 'admin':
        # Si es admin en nuestro sistema, debe ser superuser de Django
        if not usuario.is_staff or not usuario.is_superuser:
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.save(update_fields=['is_staff', 'is_superuser'])
    else:
        # Si es usuario normal, remover permisos de admin
        if usuario.is_staff or usuario.is_superuser:
            usuario.is_staff = False
            usuario.is_superuser = False
            usuario.save(update_fields=['is_staff', 'is_superuser'])


@receiver(post_save, sender=User)
def crear_perfil_y_carrito(sender, instance, created, **kwargs):
    """
    Cuando se crea un nuevo User, automáticamente se crea su PerfilUsuario y Carrito
    """
    if created:
        try:
            # Crear o obtener PerfilUsuario
            PerfilUsuario.objects.get_or_create(usuario=instance)
            # Crear Carrito
            Carrito.objects.get_or_create(usuario=instance)
        except:
            pass
