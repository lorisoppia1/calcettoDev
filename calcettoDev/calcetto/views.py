from django.shortcuts import render, redirect
from rest_framework.views import APIView
from calcetto.models import *
from rest_framework.response import Response
from rest_framework import status
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
  
class Briscola(APIView):
  
  def get(self, request):
    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = list(Developer.objects.all())
    classifica.sort(key=lambda dev: dev.briscola_win_ratio(), reverse=True)
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica}
    return render(request, "briscola.html", context)
  
class Index(APIView):
  def get(self, request):
    return render(request, "index.html")

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
    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = list(Developer.objects.all())
    classifica.sort(key=lambda dev: dev.win_perc(), reverse=True)
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica, "team1": team1, "team2": team2}
    return render(request, "calcetto.html", context)

class WinTeamMatch(APIView):

  def post(self, request, name1, name2, name3, name4):
    for dev in Developer.objects.filter(name__in=[name1, name2, name3, name4]):
      dev.total_match += 1
      dev.save()
    for dev in Developer.objects.filter(name__in=[name1, name2]):
      dev.win_match += 1
      dev.save()
    return redirect("/calcetto/")