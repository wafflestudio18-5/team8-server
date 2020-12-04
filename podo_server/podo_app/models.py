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
