from django.apps import AppConfig


class CatalogoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogo'
    verbose_name = 'Catálogo de Productos'
    
    def ready(self):
        """
        Importar los signals cuando la app está lista.
        Esto asegura que los signals se registren automáticamente.
        """
        import catalogo.models  # noqa
