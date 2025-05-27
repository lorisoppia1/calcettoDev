from django.urls import path
from calcetto.views import *

urlpatterns = [
  path('', Calcetto.as_view(), name='home'),
  path('briscola/', Briscola.as_view(), name='briscola'),
  path('win_match/<int:id>/', WinMatch.as_view(), name='win-match'),
  path('lost_match/<int:id>/', LostMatch.as_view(), name='remove-point'),
  path('briscola_win_match/<int:id>/', BriscolaWinMatch.as_view(), name='briscola-win-match'),
  path('briscola_lost_match/<int:id>/', BriscolaLostMatch.as_view(), name='briscola-lost-match'),
  path('random_match/', RandomMatch.as_view(), name='random-match'),
  path('win_team_match/<str:name1>/<str:name2>/<str:name3>/<str:name4>/', WinTeamMatch.as_view(), name='win-team-match'),
  path("classifica/", ClassificaAPI.as_view(), name="classifica-api"),
  path("random/", RandomAPI.as_view(), name="random-api"),
  path("all_matches/", MatchesAPI.as_view(), name="matches-api"),
  path("create_match/", MatchesAPI.as_view(), name="create-match-api"),
  path("get_match/<int:id>/", MatchAPI.as_view(), name="match-api"),
  path("edit_params/<int:id>/", EditParamsAPI.as_view(), name="edit-params"),
  path('singolo/', CalcettoSingolo.as_view(), name='index-singolo'),
  path('pitagora/', Pitagora.as_view(), name='pitagora'),
]