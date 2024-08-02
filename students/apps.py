from django.apps import AppConfig

class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
    
    def ready(self):
        # Import signals to ensure they are registered
        import students.signals
        # Import custom filters if necessary
        from students import custome_filters
