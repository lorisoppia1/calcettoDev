from django.urls import path
from calcetto.views import *

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('add_point/<int:id>/', AddPoints.as_view(), name='add-point'),
  path('remove_point/<int:id>/', RemovePoints.as_view(), name='remove-point'),
]