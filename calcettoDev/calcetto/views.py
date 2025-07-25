from django.shortcuts import render, redirect
from rest_framework.views import APIView
from calcetto.models import *
from rest_framework.response import Response
from rest_framework import status
from calcetto.serializers import *
from django.db.models import Q, F, ExpressionWrapper, FloatField
from itertools import combinations
import random, requests

class Calcetto(APIView):

  def get(self, request):
    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = list(Developer.objects.all())
    classifica.sort(key=lambda dev: dev.win_perc(), reverse=True)
    res = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/today").json()
    res2 = requests.get("https://v2.jokeapi.dev/joke/Any").json()
    if res2["type"] == "single":
      joke2 = res2["joke"]
    else:
      joke2 = res2["setup"] + "\n" + res2["delivery"]
    res3 = requests.get("https://random-d.uk/api/v2/random").json()
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica, "joke": res["text"], "joke2": joke2, "joke3": res3["url"]}
    return render(request, "calcetto.html", context)

class CalcettoSingolo(APIView):

  def get(self, request):
    developers1 = Developer.objects.all().order_by("name")[:7]
    developers2 = Developer.objects.all().order_by("name")[7:]
    context = {"developers1": developers1, "developers2": developers2}
    return render(request, "calcetto_singolo.html", context)


class ClassificaAPI(APIView):

  def get(self, request):
    classifica = Developer.objects.annotate(win_percentage=ExpressionWrapper(F('win_match') * 100 / F('total_match'), output_field=FloatField())).order_by('-win_percentage')
    serializer = DeveloperSerializers(classifica, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class Briscola(APIView):

  def get(self, request):
    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = list(Developer.objects.all())
    classifica.sort(key=lambda dev: dev.briscola_win_ratio(), reverse=True)
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica}
    return render(request, "briscola.html", context)

class WinMatch(APIView):

  def post(self, request, id):
    developer = Developer.objects.get(id=id)
    developer.total_match += 1
    developer.win_match += 1
    developer.save()
    return redirect("/calcetto/")

class LostMatch(APIView):

  def post(self, request, id):
    developer = Developer.objects.get(id=id)
    developer.total_match += 1
    developer.save()
    return redirect("/calcetto/")

class BriscolaWinMatch(APIView):

  def post(self, request, id):
    developer = Developer.objects.get(id=id)
    developer.briscola_total_match += 1
    developer.briscola_win_match += 1
    developer.save()
    return redirect("/calcetto/briscola/")

class BriscolaLostMatch(APIView):

  def post(self, request, id):
    developer = Developer.objects.get(id=id)
    developer.briscola_total_match += 1
    developer.save()
    return redirect("/calcetto/briscola/")

class RandomMatch(APIView):

  def post(self, request):
    data = dict(request.data)
    players = list(Developer.objects.filter(id__in=data["randoms"]))

    random.shuffle(players)
    team1 = [players[0], players[1]]
    team2 = [players[2], players[3]]

    # → invio notifica Slack con compagni
    SLACK_TOKEN = 'xoxb-4707778244432-4683996066467-lyH4DSbJJ0cZGf8MGCMvrHBj'
    headers = {
      'Authorization': f'Bearer {SLACK_TOKEN}',
      'Content-Type': 'application/json'
    }
    for player in team1 + team2:
      if not player.slack_id:
        continue
      # calcolo nomi compagni
      squad = team1 if player in team1 else team2
      mates = [p.name for p in squad if p.id != player.id]
      mates_str = " e ".join(mates)
      opponents = team2 if squad is team1 else team1
      opponents_names = [p.name for p in opponents]
      opponents_str = " e ".join(opponents_names)
      payload = {
        "channel": player.slack_id,
        "text": f"👋 Ciao {player.name}, sei il prescelto!!!",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": f"👋 Ciao {player.name}, sei in squadra con {mates_str} e giocherai contro {opponents_str}!",
            }
          }
        ]
      }
      resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        json=payload
      )
      if not resp.ok or not resp.json().get("ok"):
        print(f"Slack error for {player.name}: {resp.text}")

    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = list(Developer.objects.all())
    classifica.sort(key=lambda dev: dev.win_perc(), reverse=True)
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica, "team1": team1, "team2": team2}
    return render(request, "calcetto.html", context)

class RandomAPI(APIView):

  def post(self, request):
    randoms = Developer.objects.filter(id__in=request.data["randoms"]).order_by("?")
    serializer = DeveloperSerializers(randoms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class WinTeamMatch(APIView):

  def post(self, request, name1, name2, name3, name4):
    for dev in Developer.objects.filter(name__in=[name1, name2, name3, name4]):
      dev.total_match += 1
      dev.save()
    for dev in Developer.objects.filter(name__in=[name1, name2]):
      dev.win_match += 1
      dev.save()
    return redirect("/calcetto/")

class MatchesAPI(APIView):

  def get(self, request):
    matches = Match.objects.all()
    serializer = MatchSerializers(matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def post(self, request):
    # {"winner_1": 1, "winner_2": 2, "loser_1": 3, "loser_2": 4}
    winner_1 = Developer.objects.get(id=request.data["winner_1"])
    winner_1.total_match += 1
    winner_1.win_match += 1
    winner_1.save()
    winner_2 = Developer.objects.get(id=request.data["winner_2"])
    winner_2.total_match += 1
    winner_2.win_match += 1
    winner_2.save()
    loser_1 = Developer.objects.get(id=request.data["loser_1"])
    loser_1.total_match += 1
    loser_1.save()
    loser_2 = Developer.objects.get(id=request.data["loser_2"])
    loser_2.total_match += 1
    loser_2.save()
    Match.objects.create(
      winner_1 = winner_1,
      winner_2 = winner_2,
      loser_1 = loser_1,
      loser_2 = loser_2,
      )
    return Response(status=status.HTTP_200_OK)

class MatchAPI(APIView):

  def get(self, request, id):
    developer = Developer.objects.get(id=id)
    matches = Match.objects.filter(Q(winner_1=developer) | Q(winner_2=developer) | Q(loser_1=developer) | Q(loser_2=developer)).distinct()
    serializer = MatchSerializers(matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class EditParamsAPI(APIView):

  def post(self, request, id):
    developer = Developer.objects.get(id=id)
    new_params = request.data["new_params"]
    developer.params = new_params
    developer.save()
    serializer = DeveloperSerializers(developer, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

class Pitagora(APIView):

  def get(self, request):
    # fai nostri servizi con 6 figure geometriche (cerchio. triangolo e quadrato) o foto, logopedia, psicoterapia, psicologia dell'eta evolutiva
    # TNPEE, osteopatia D.O. e chinesiologia, massoterapia

    # nella parte Un luogo di ascolto e supporto metti un tube tipo londra in css con 6 fermate

    # metti invio mail alessandro@logopedistarigamonti.com nel prenota

    # nella home metto studio pitagora con il font e sotto servizi rieducativi e riabilitativi al centro

    # fai uguale fino a formazione esclusa.
    return render(request, "pitagora4.html")
  
class Torneo(APIView):

  def get(self, request):
    developers = Developer.objects.all()
    context = {"developers": developers}
    return render(request, "torneo.html", context=context)

class TorneoRandom(APIView):

  def post(self, request):
    data = dict(request.data)
    players = list(Developer.objects.filter(id__in=data["randoms"]))
    random.shuffle(players)
    num_teams = int(len(players) / 2)
    response = {"teams": {}, "matches": []}
    for i in range(num_teams):
      response["teams"][f"team_{i+1}"] = {
        "player_1" : {"id": players[i*2].id, "name":players[i*2].name},
        "player_2" : {"id": players[i*2+1].id, "name":players[i*2+1].name},
      }
    
    team_ids = list(response["teams"].keys())
    andata = []
    ritorno = []

    for team1, team2 in combinations(team_ids, 2):
        andata.append({"home": team1, "away": team2})
        ritorno.append({"home": team2, "away": team1})

    response["matches"] = andata + ritorno
    return Response(response, status=status.HTTP_200_OK)
