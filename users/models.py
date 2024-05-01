from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

from shared.models import BaseModel


class User(BaseModel, AbstractUser):
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True, db_index=True)
    image = models.ImageField(upload_to='user_images/', default='default.jpg', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])
    ])
    followers = models.ManyToManyField('users.User', blank=True)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def __str__(self):
        return self.username


class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} requested to {self.to_user}"
