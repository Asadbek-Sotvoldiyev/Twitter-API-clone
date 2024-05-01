from django.urls import path
from .views import (PostCreateApiView, GetAllPostsListApiView, GetUserPostApiView,
                    MyAllPostsApiView, PostUpdateApiView, PostDestroyApiView, AddCommentApiView,
                    GetAllPostComments, DestroyComment, AllMyCommentsApiView, AddLikeApiView, GetUsersWhoLiked)

urlpatterns = [
    # posts
    path('create/', PostCreateApiView.as_view()),
    path('get-all-posts/', GetAllPostsListApiView.as_view()),
    path('user-posts/<int:id>/', GetUserPostApiView.as_view()),
    path('all-my-posts/', MyAllPostsApiView.as_view()),
    path('update-post/<int:pk>/', PostUpdateApiView.as_view()),
    path('delete-post/<int:pk>/', PostDestroyApiView.as_view()),

    # Comments
    path('add-comment/', AddCommentApiView.as_view()),
    path('get-all-post-comments/<int:post_id>/', GetAllPostComments.as_view()),
    path('delete-comment/<int:pk>/', DestroyComment.as_view()),
    path('all-my-comments/', AllMyCommentsApiView.as_view()),

    # Likes
    path('add-like/', AddLikeApiView.as_view()),
    path('get-users-who-liked/<int:post_id>/', GetUsersWhoLiked.as_view())
]
