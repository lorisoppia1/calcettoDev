from django.urls import path
from calcetto.views import *

urlpatterns = [
  path('', Calcetto.as_view(), name='home'),
  path('index/', Index.as_view(), name='index'),
  path('briscola/', Briscola.as_view(), name='briscola'),
  path('win_match/<int:id>/', WinMatch.as_view(), name='win-match'),
  path('lost_match/<int:id>/', LostMatch.as_view(), name='remove-point'),
  path('briscola_win_match/<int:id>/', BriscolaWinMatch.as_view(), name='briscola-win-match'),
  path('briscola_lost_match/<int:id>/', BriscolaLostMatch.as_view(), name='briscola-lost-match'),
  path('random_match/', RandomMatch.as_view(), name='random-match'),
  path('win_team_match/<str:name1>/<str:name2>/<str:name3>/<str:name4>/', WinTeamMatch.as_view(), name='win-team-match'),
]