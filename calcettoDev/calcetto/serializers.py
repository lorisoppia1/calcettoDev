from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField
from calcetto.models import *

class DeveloperSerializers(ModelSerializer):

  class Meta:
      model = Developer
      fields = ['id','name','total_match','win_match','image_url','win_perc']
