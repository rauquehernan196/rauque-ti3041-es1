"""
Comando personalizado para Django que permite gestionar roles de usuarios.

Uso:
    python manage.py cambiar_rol usuario1 admin
    python manage.py cambiar_rol usuario1 usuario
    python manage.py cambiar_rol --list
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from catalogo.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Cambiar el rol de un usuario (usuario/admin)'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            nargs='?',
            type=str,
            help='Nombre de usuario a modificar'
        )
        parser.add_argument(
            'rol',
            nargs='?',
            type=str,
            choices=['usuario', 'admin'],
            help='Nuevo rol: usuario o admin'
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='Listar todos los usuarios y sus roles'
        )

    def handle(self, *args, **options):
        # Si se pide listar usuarios
        if options['list']:
            self.listar_usuarios()
            return

        # Validar que se proporcionó username y rol
        if not options['username'] or not options['rol']:
            raise CommandError(
                '❌ Debes proporcionar username y rol.\n'
                '   Uso: python manage.py cambiar_rol usuario1 admin'
            )

        username = options['username']
        nuevo_rol = options['rol']

        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'❌ Usuario "{username}" no existe')

        # Obtener o crear el perfil
        perfil, creado = PerfilUsuario.objects.get_or_create(usuario=usuario)
        rol_anterior = perfil.rol

        # Cambiar el rol
        perfil.rol = nuevo_rol
        perfil.save()

        # Mostrar resultado
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Rol actualizado exitosamente:\n'
            f'   Usuario: {username}\n'
            f'   Rol anterior: {rol_anterior}\n'
            f'   Rol nuevo: {nuevo_rol}\n'
        ))

    def listar_usuarios(self):
        """Lista todos los usuarios con sus roles y permisos"""
        self.stdout.write(self.style.SUCCESS(
            '\n' + '=' * 80
        ))
        self.stdout.write(self.style.SUCCESS(
            '👥 USUARIOS Y ROLES'
        ))
        self.stdout.write(self.style.SUCCESS(
            '=' * 80 + '\n'
        ))

        usuarios = User.objects.all()

        if not usuarios.exists():
            self.stdout.write(self.style.WARNING('No hay usuarios registrados.'))
            return

        for usuario in usuarios:
            try:
                rol = usuario.perfil.rol
                es_admin = usuario.perfil.es_admin()
            except PerfilUsuario.DoesNotExist:
                rol = 'sin perfil'
                es_admin = False

            # Formatear información
            nombre_completo = usuario.get_full_name() or usuario.username
            tipo_usuario = '👑 ADMIN' if es_admin else '👤 USUARIO'
            staff_status = '✓ is_staff' if usuario.is_staff else '✗ is_staff'
            superuser_status = '✓ is_superuser' if usuario.is_superuser else '✗ is_superuser'

            self.stdout.write(
                f'{tipo_usuario} | {usuario.username:15} | {nombre_completo:20} | '
                f'{staff_status:15} | {superuser_status:15}'
            )

        self.stdout.write(self.style.SUCCESS(
            '\n' + '=' * 80 + '\n'
        ))
