from django.contrib import admin
from .models import Message, Profile, FriendRequest




# Register your models here.
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(FriendRequest)