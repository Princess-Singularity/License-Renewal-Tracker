from django.apps import AppConfig


class DatabaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DATABASE_APP'
    verbose_name = 'Database App'
