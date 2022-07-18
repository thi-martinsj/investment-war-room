from django.apps import AppConfig


class AssetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assets'

    def ready(self) -> None:
        from .views import insert_assets
        from . import scheduler

        insert_assets()
        scheduler.start()
