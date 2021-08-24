from django.contrib import admin
from django.urls import path, include

from system.apis import HealthCheckAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('system/', include('system.urls')),
    path('health', HealthCheckAPI.as_view()),
]
