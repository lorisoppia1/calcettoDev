from django.contrib import admin
from calcetto.models import Developer

class DeveloperAdmin(admin.ModelAdmin):
  list_display = ["name","total_points"]

admin.site.register(Developer)
