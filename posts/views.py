from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


# Post yaratish
class PostCreateApiView(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Brcha postlarni ko'rish
class GetAllPostsListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Biror userning barcha postlarini ko'rish
class GetUserPostApiView(APIView):
    def get(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            posts = Post.objects.filter(user=user)
            serializer = PostSerializer(posts, many=True)
        except:
            data = {
                'success': False,
                "message": "Bunday foydalanuvchi mavjud emas!"
            }
            raise ValidationError(data)

        return Response(serializer.data)


class MyAllPostsApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


# Postni yangilash, o'zi yaratgan postni yangilay oladi
class PostUpdateApiView(UpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = {
            'success': True,
            'message': 'Post updated successfully',
        }

        return Response(data, status=status.HTTP_200_OK)


# Postni o'chirish, o'zi yaratgan postni o'chira oladi
class PostDestroyApiView(DestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({'success': True, 'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Kommentariya qoldirish
class AddCommentApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)


# Postga qoldirilgan barcha kommentariyalarni ko'rish
class GetAllPostComments(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)


class DestroyComment(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAdminUser, )
    serializer_class = CommentSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({'success': True, 'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Men qoldirgan barcha commentlar
class AllMyCommentsApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


# Like bosish
class AddLikeApiView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        try:
            id = request.data['id']
            post = Post.objects.get(id=id)
            post.liked_users.add(request.user)
            data = {
                "success": True,
                "message": f"Post is liked",
                "post_id": post.id,
                "post_content": post.content
            }
        except:
            data = {
                "success": False,
                "message": "Post doesn't exist"
            }
        return Response(data)


# Postga like bosgan barcha userlarni olish
class GetUsersWhoLiked(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Post.objects.get(id=post_id).liked_users.prefetch_related()


# Men yoqtirgan barcha postlar
class MyLikedPostsApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(liked_users=self.request.user)
