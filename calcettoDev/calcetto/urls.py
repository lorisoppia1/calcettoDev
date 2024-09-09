from django.urls import path
from calcetto.views import *

urlpatterns = [
  path('', Home.as_view(), name='home'),
]