from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'video_or_photo', 'content')

    def to_representation(self, instance):
        data = {
            'status': True,
            'post': {
                'id': instance.id,
                'user': instance.user.username,
                'video_or_photo': instance.video_or_photo.url if instance.video_or_photo else None,
                'content': instance.content,
            }
        }
        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'text')

    def to_representation(self, instance):
        data = {
            "success": True,
            "message": "Commented successfully",
            "user_id": instance.user.id,
            "post_id": instance.post.id,
            'comment_id': instance.id,
            "comment text": instance.text
        }
        return data
