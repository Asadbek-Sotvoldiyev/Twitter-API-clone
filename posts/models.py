from django.core.validators import FileExtensionValidator
from django.db import models
from users.models import User
from shared.models import BaseModel


class Post(BaseModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    video_or_photo = models.FileField(upload_to='post_files/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'avi', 'wmv'])])
    content = models.TextField()
    liked_users = models.ManyToManyField(User)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_time}"


class Comment(BaseModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username} commented to {self.post.content}"






