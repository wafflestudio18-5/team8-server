from django.db import models
from django.contrib.auth.models import User
import os

def profileImagePath(instance, filename):
  ext = filename.split('.')[-1]
  filename =  '{}.{}'.format(instance.pk, ext)
  return os.path.join('profile', filename)

def productImagePath(instance, filename):
  ext = filename.split('.')[-1]
  filename =  '{}.{}'.format(instance.pk, ext)
  return os.path.join('product', filename)

class TimeModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  class Meta:
    abstract = True

class Profile(TimeModel):
  user = models.ForeignKey(User, related_name='profile',on_delete=models.CASCADE)
  nickname = models.CharField(max_length=100)
  temperature = models.FloatField(default=36.5)
  image = models.ImageField(upload_to=profileImagePath)
  image_url = models.URLField(null=True)
  products_sold= models.IntegerField(default=0)
  products_bought= models.IntegerField(default=0)


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
  status = models.PositiveIntegerField(default=2)
  seller = models.ForeignKey(Profile, related_name='selling_products',on_delete=models.SET_NULL, null=True)
  buyer = models.ForeignKey(Profile, related_name='bought_products',on_delete=models.SET_NULL, null=True)
  
  count_comments = models.PositiveSmallIntegerField(default=0)
  count_likes = models.PositiveSmallIntegerField(default=0)
  count_views = models.PositiveSmallIntegerField(default=0)

  city = models.ForeignKey(City, related_name='here_products',on_delete=models.SET_NULL, null=True)
  distance_range = models.PositiveSmallIntegerField(default=0)

class ProductImage(TimeModel):
  product = models.ForeignKey(Product, related_name='images',on_delete=models.CASCADE)
  image = models.ImageField(upload_to=productImagePath)
  image_url = models.URLField(null=True)

class LikeProduct(TimeModel):
  profile = models.ForeignKey(Profile, related_name='like_products',on_delete=models.SET_NULL, null=True)
  product = models.ForeignKey(Product, related_name='like_profiles',on_delete=models.SET_NULL, null=True)
  active = models.BooleanField(default=True)

class ChatRoom(TimeModel):
  product = models.ForeignKey(Product, related_name='chatrooms',on_delete=models.SET_NULL, null=True)
  will_buyer = models.ForeignKey(Profile, related_name='chatrooms',on_delete=models.SET_NULL, null=True)
  is_active = models.BooleanField(default=True)
  class Meta:
    unique_together = (
      ('product','will_buyer'),
    )

class Transaction():
  chatroom = models.ForeignKey(ChatRoom, related_name='appointment', on_delete=models.SET_NULL) 
  seller_review = PositiveSmallIntegerField(default=0)
  buyer_review = PositiveSmallIntegerField(default=0)


class SuggestPrice():
  suggest_price = models.PositiveSmallIntegerField()
  will_buyer = models.ForeignKey(Profile, related_name='suggest_price', on_delete=models.SET_NULL, null=True)
  confirm = models.BooleanField(default=False)
  chatroom = models.ForeignKey(ChatRoom, related_name='suggest_price', on_delete=models.SET_NULL)
