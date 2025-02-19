from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("base.urls")),
    path('api/payments/', include('base.urls')),
]