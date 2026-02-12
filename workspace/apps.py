from django.apps import AppConfig

class WorkspacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workspace'

    def ready(self):
        import workspace.signals
