from django.contrib import admin

from podo_app.models import Profile, City, ProfileCity, Product, LikeProduct, ChatRoom, Message
# Register your models here.

admin.site.register(Profile)
admin.site.register(City)
admin.site.register(ProfileCity)
admin.site.register(Product)
admin.site.register(LikeProduct)
admin.site.register(ChatRoom)
admin.site.register(Message)