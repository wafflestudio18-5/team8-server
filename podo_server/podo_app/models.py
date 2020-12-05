from django.db import models
from django.contrib.auth.models import User

class TimeModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  class Meta:
    abstract = True

class Profile(TimeModel):
  user = models.ForeignKey(User, related_name='profile',on_delete=models.CASCADE)
  nickname = models.CharField(max_length=100)
  temperature = models.FloatField(default=36.5)

class City(TimeModel):
  name = models.CharField(max_length=100)
  location = models.CharField(max_length=100)

class  ProfileCity(TimeModel):
  profile = models.ForeignKey(Profile, related_name='profile_cities',on_delete=models.CASCADE)
  city = models.ForeignKey(City, related_name='profile_cities',on_delete=models.CASCADE)
  