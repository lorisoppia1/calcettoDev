from django.db import models

class Developer(models.Model):

  name = models.CharField(max_length=100)
  total_points = models.IntegerField(default=0)
  total_match = models.IntegerField(default=0)
  win_match = models.IntegerField(default=0)
  image_url = models.CharField(max_length=500, default="")

  def __str__(self):
    return f"{self.name} - {self.total_points}"
    # pass admin 6zJ1a3ly

  def win_ratio(self):
    if self.total_match != 0:
      return round((self.win_match * 100 / self.total_match), 2)
    return 0
