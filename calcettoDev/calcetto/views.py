from django.shortcuts import render
from rest_framework.views import APIView
from calcetto.models import *

class Home(APIView):
  
  def get(self, request):
    developers = Developer.objects.all()
    context = {"developers": developers}
    return render(request, "home.html", context)

