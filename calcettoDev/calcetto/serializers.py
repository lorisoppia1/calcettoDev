from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from calcetto.models import *

class DeveloperSerializers(ModelSerializer):

  class Meta:
      model = Developer
      fields = "__all__"

class MatchSerializers(ModelSerializer):
  winner_1 = DeveloperSerializers()
  winner_2 = DeveloperSerializers()
  loser_1 = DeveloperSerializers()
  loser_2 = DeveloperSerializers()

  class Meta:
      model = Match
      fields = ["winner_1","winner_2","loser_1","loser_2","day"]
