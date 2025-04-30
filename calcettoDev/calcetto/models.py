from django.db import models
import math

class Developer(models.Model):

  name = models.CharField(max_length=100)
  description = models.TextField(default="")
  total_match = models.IntegerField(default=0)
  win_match = models.IntegerField(default=0)
  image_url = models.CharField(max_length=500, default="")
  briscola_total_match = models.IntegerField(default=0)
  briscola_win_match = models.IntegerField(default=0)
  params = models.JSONField(default=dict, blank=True, null=True)
  total_match_singolo = models.IntegerField(default=0)
  win_match_singolo = models.IntegerField(default=0)
  slack_id = models.CharField(max_length=100, default="")

  def __str__(self):
    return self.name
    # pass admin 6zJ1a3ly

  def win_ratio(self):
    if self.total_match != 0:
      # ratio = (1 + self.win_match / self.total_match) * (math.log(self.total_match + 1))
      ratio = 1 * self.win_match / (math.log(1 * self.total_match) + 1)
      return round(ratio, 2)
    return 0.0

  def win_perc(self):
    if self.total_match != 0:
      return round((self.win_match * 100 / self.total_match), 2)
    return 0.0

  def win_perc_singolo(self):
    if self.total_match_singolo != 0:
      return round((self.win_match_singolo * 100 / self.total_match_singolo), 2)
    return 0.0

  def briscola_win_ratio(self):
    if self.briscola_total_match != 0:
      return round((self.briscola_win_match * 100 / self.briscola_total_match), 2)
    return 0.0

class Match(models.Model):

  winner_1 = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name="matches_winner_1")
  winner_2 = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name="matches_winner_2")
  loser_1 = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name="matches_loser_1")
  loser_2 = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name="matches_loser_2")
  day = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    if self.winner_1 and self.winner_2 and self.loser_1 and self.loser_2:
      return f"{self.winner_1.name} - {self.winner_2.name} - {self.loser_1.name} - {self.loser_2.name} - {str(self.day)}"
    return ""
