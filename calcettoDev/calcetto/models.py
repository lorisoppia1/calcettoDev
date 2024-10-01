from django.db import models
import math

class Developer(models.Model):

  name = models.CharField(max_length=100)
  total_match = models.IntegerField(default=0)
  win_match = models.IntegerField(default=0)
  image_url = models.CharField(max_length=500, default="")
  briscola_total_match = models.IntegerField(default=0)
  briscola_win_match = models.IntegerField(default=0)

  def __str__(self):
    return self.name
    # pass admin 6zJ1a3ly

  def win_ratio(self):
    if self.total_match != 0:
      ratio = (1 + self.win_match / self.total_match) * (math.log(self.total_match + 1))
      return round(ratio, 2)
    return 0.0
  
  def win_perc(self):
    if self.total_match != 0:
      return round((self.win_match * 100 / self.total_match), 2)
    return 0.0
  
  def briscola_win_ratio(self):
    if self.briscola_total_match != 0:
      return round((self.briscola_win_match * 100 / self.briscola_total_match), 2)
    return 0.0

