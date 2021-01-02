from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
import json

class PostProductCase(TestCase):
    client=Client()