from django.contrib import admin

from podo_app.models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(City)
admin.site.register(ProfileCity)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(LikeProduct)
admin.site.register(ChatRoom)