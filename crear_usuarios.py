import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from catalogo.models import PerfilUsuario

print("=" * 60)
print("🛠️  CREANDO USUARIOS DE DEMOSTRACIÓN")
print("=" * 60)

# Eliminar usuarios de demostración existentes si existen
User.objects.filter(username__in=['usuario1', 'admin']).delete()

# ============================================================
# 1. CREAR USUARIO NORMAL
# ============================================================
print("\n📝 Creando usuario normal...")
usuario_normal = User.objects.create_user(
    username='usuario1',
    email='usuario@ejemplo.com',
    password='Password123!',
    first_name='Juan',
    last_name='Pérez',
    is_staff=False,
    is_superuser=False
)
# El signal se encargará de crear el PerfilUsuario
print("✅ Usuario normal creado:")
print(f"   Username: usuario1")
print(f"   Email: usuario@ejemplo.com")
print(f"   Contraseña: Password123!")
print(f"   Rol: Usuario Normal")

# ============================================================
# 2. CREAR USUARIO ADMINISTRADOR (TAMBIÉN SERÁ SUPERUSER)
# ============================================================
print("\n👑 Creando usuario administrador...")
admin_user = User.objects.create_user(
    username='admin',
    email='admin@ejemplo.com',
    password='Admin123!',
    first_name='Administrador',
    last_name='Sistema',
    is_staff=True,        # Esto permite acceder a /admin/
    is_superuser=True     # Esto da permisos totales
)

# Actualizar el perfil para que también sea admin en nuestro sistema
perfil_admin = PerfilUsuario.objects.get(usuario=admin_user)
perfil_admin.rol = 'admin'
perfil_admin.save()

print("✅ Usuario administrador creado:")
print(f"   Username: admin")
print(f"   Email: admin@ejemplo.com")
print(f"   Contraseña: Admin123!")
print(f"   Rol: Administrador")
print(f"   Permisos: Acceso a /admin/ y /admin/panel/")

# ============================================================
# VERIFICACIÓN
# ============================================================
print("\n" + "=" * 60)
print("📊 VERIFICACIÓN")
print("=" * 60)

usuario1 = User.objects.get(username='usuario1')
admin = User.objects.get(username='admin')

print(f"\n👤 USUARIO NORMAL (usuario1):")
print(f"   is_staff: {usuario1.is_staff}")
print(f"   is_superuser: {usuario1.is_superuser}")
print(f"   Rol: {usuario1.perfil.rol}")
print(f"   Es admin: {usuario1.perfil.es_admin()}")

print(f"\n👑 ADMINISTRADOR (admin):")
print(f"   is_staff: {admin.is_staff}")
print(f"   is_superuser: {admin.is_superuser}")
print(f"   Rol: {admin.perfil.rol}")
print(f"   Es admin: {admin.perfil.es_admin()}")

print("\n" + "=" * 60)
print("✨ ¡Usuarios creados exitosamente!")
print("=" * 60)
print("\n🔗 URLS DE ACCESO:")
print("   Landing:      http://127.0.0.1:8000/")
print("   Login:        http://127.0.0.1:8000/login/")
print("   Catálogo:     http://127.0.0.1:8000/catalogo/ (requiere login)")
print("   Panel Admin:  http://127.0.0.1:8000/admin/panel/ (solo admin)")
print("   Django Admin: http://127.0.0.1:8000/admin/ (solo admin/superuser)")
print("\n")
