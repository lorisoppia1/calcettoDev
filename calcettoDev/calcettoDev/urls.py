from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('calcetto/', include('calcetto.urls')),
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('/calcetto')),
]
