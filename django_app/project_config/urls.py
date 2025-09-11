
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app_monitor.views import ilk_def,addRecordArduino,django_device,addEventArduino

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("app_monitor.urls")),
    path('app_monitor/',include("app_monitor.urls")),
    path('core/',include("core.urls")),
    path('app_monitor/ilk_def',ilk_def,name="ilk_def"),
    path('addRecordArduino',addRecordArduino,name="addRecordArduino"),
    path('addEventArduino',addEventArduino,name="addEventArduino"),
    #USER
    path("user/",include('app_user_profile.urls',namespace="app_user_profile")  ),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static_files')