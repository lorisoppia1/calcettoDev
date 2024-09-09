from django.urls import path
from calcetto.views import *

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('add_point/<int:id>/', AddPoints.as_view(), name='add-point'),
  path('remove_point/<int:id>/', RemovePoints.as_view(), name='remove-point'),
  path('win_match/<int:id>/', WinMatch.as_view(), name='win-match'),
  path('lost_match/<int:id>/', LostMatch.as_view(), name='remove-point'),
]