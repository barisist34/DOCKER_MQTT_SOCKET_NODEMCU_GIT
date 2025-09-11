from django.apps import AppConfig
# from django.contrib.auth.models import User  # USER satırı olduğunda django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet. hatası alınıyor.
# from .tasks import notify_user

class AppMonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_monitor'
    # def ready(self): #241224
    #         from .scheduler import scheduler
    #         scheduler.start()
    # def ready(self):
    #     # from .tasks import notify_task_1
    #     from .tasks import notify_user
    #     # notify_user(user.id)
    #     # notify_user(1)
    #     notify_user(1,repeat=20)
    # #     # notify_task_1(1)
