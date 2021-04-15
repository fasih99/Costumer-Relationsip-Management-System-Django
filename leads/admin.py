from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.

from .models import User,UserProfile,Agent,Lead,Category

admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(UserProfile) 
admin.site.register(Category)

