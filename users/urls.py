from django.urls import path
from .views import (RegisterApiView, LoginApiView, GetAllUsersListApiView,
                    SendFollowRequestApiView, MyFollowRequestsApiView, AcceptFollowRequestApiView,
                    DeleteFollowRequestApiView, IgnoreFollowRequestApiView, MyAllFollowersListApiView, LoginRefreshView,
                    LogOutView)

urlpatterns = [
    # auth
    path('register/', RegisterApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('get-all-users/', GetAllUsersListApiView.as_view()),

    # followers
    path('send-follow-request/', SendFollowRequestApiView.as_view()),
    path('my-all-follow-requests/', MyFollowRequestsApiView.as_view()),
    path('accept-follower/', AcceptFollowRequestApiView.as_view()),
    path('delete-follower/<int:id>/', DeleteFollowRequestApiView.as_view()),
    path('ignore-follower/', IgnoreFollowRequestApiView.as_view()),
    path('my-followers/', MyAllFollowersListApiView.as_view()),
]