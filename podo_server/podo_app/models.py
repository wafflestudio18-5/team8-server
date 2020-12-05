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
  
class Product(TimeModel):
  name = models.CharField(max_length=100)
  category = models.CharField(max_length=50)
  price = models.PositiveIntegerField()
  allow_suggest = models.BooleanField()
  status = models.CharField(max_length=50)
  seller = models.ForeignKey(Profile, related_name='selling_products',on_delete=models.SET_NULL, null=True)
  buyer = models.ForeignKey(Profile, related_name='bought_products',on_delete=models.SET_NULL, null=True)
  
  count_comments = models.PositiveSmallIntegerField(default=0)
  count_likes = models.PositiveSmallIntegerField(default=0)
  count_views = models.PositiveSmallIntegerField(default=0)

  city = models.ForeignKey(City, related_name='here_products',on_delete=models.SET_NULL, null=True)
  distance_range = models.PositiveSmallIntegerField(default=0)

class LikeProduct(TimeModel):
  profile = models.ForeignKey(Profile, related_name='like_products',on_delete=models.SET_NULL, null=True)
  product = models.ForeignKey(Product, related_name='like_profiles',on_delete=models.SET_NULL, null=True)
