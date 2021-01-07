"""podo_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from django.urls import include, path
from podo_server.views import *
from django.urls import path, include

app_name = 'product'

router = SimpleRouter()
router.register('product', ProductViewSet, basename='product')
router.register('chatroom', ChatRoomViewSet, basename='chatroom')

urlpatterns = [
    path('', ping),
    path('', include((router.urls))),
    path('api/v1/', include('user.urls')),
    path('admin/', admin.site.urls),
]
