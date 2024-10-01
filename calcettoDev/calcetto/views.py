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
    classifica.sort(key=lambda dev: dev.win_ratio(), reverse=True)
    res = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/today")
    joke = res.json()["text"]
    res2 = requests.get("https://v2.jokeapi.dev/joke/Any?contains=sex")
    res2_json = res2.json()
    if res2_json["type"] == "single":
      joke2 = res2_json["joke"]
    else:
      joke2 = res2_json["setup"] + "\n" + res2_json["delivery"]
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica, "joke": joke, "joke2": joke2}
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
    players1 = f"{players[0].name} - {players[1].name}"
    players2 = f"{players[2].name} - {players[3].name}"
    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = list(Developer.objects.all())
    classifica.sort(key=lambda dev: dev.win_ratio(), reverse=True)
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica, "players1": players1, "players2": players2}
    return render(request, "calcetto.html", context)
