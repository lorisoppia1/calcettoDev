from django.shortcuts import render, redirect
from rest_framework.views import APIView
from calcetto.models import *

class Home(APIView):
  
  def get(self, request):
    developers1 = Developer.objects.all().order_by("name")[:6]
    developers2 = Developer.objects.all().order_by("name")[6:]
    classifica = Developer.objects.order_by("-total_points")[:3]
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
