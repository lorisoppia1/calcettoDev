from django.contrib import admin
from calcetto.models import *

class DeveloperAdmin(admin.ModelAdmin):
  list_display = ["name"]

class MatchAdmin(admin.ModelAdmin):
  list_display = ["winner_1","winner_2","loser_1","loser_2","day"]

admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Match, MatchAdmin)
