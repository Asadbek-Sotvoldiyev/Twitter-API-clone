from django.contrib import admin
from .models import User, FollowRequest

admin.site.register([User, FollowRequest])
