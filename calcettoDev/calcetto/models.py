from django.db import models

class Developer(models.Model):

  name = models.CharField(max_length=100)
  description = models.CharField(max_length=255, default="")
  total_points = models.IntegerField(default=0)

  def __str__(self):
    return f"{self.name} - {self.total_points}"
    # pass admin 6zJ1a3ly
