from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda req: redirect('/calcetto')),
    path('calcetto/', include('calcetto.urls')),
    path('admin/', admin.site.urls),
]
