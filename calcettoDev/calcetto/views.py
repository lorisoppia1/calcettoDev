from django.shortcuts import render, redirect
from rest_framework.views import APIView
from calcetto.models import *
from django.db.models import F, FloatField
from django.db.models.functions import Cast, Round

class Home(APIView):
  
  def get(self, request):
    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = list(Developer.objects.all())
    # developers = Developer.objects.annotate(win_ratio=Round(Cast(F('win_match'), FloatField()) / Cast(F('total_match'), FloatField()), 2)).order_by('-win_ratio')
    classifica.sort(key=lambda dev: dev.win_ratio(), reverse=True)
    context = {"developers1": developers1, "developers2": developers2, "classifica": classifica}
    return render(request, "home.html", context)
  
class AddPoints(APIView):

  def post(self, request, id):
    developer = Developer.objects.get(id=id)
    developer.total_points += 1
    developer.save()
    return redirect("/calcetto/")

class RemovePoints(APIView):

  def post(self, request, id):
    developer = Developer.objects.get(id=id)
    developer.total_points -= 1
    developer.save()
    return redirect("/calcetto/")

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