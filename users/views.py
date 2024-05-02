from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework import permissions, status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, FollowRequestSerializer
from .models import User, FollowRequest


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginApiView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            data = {
                "success": True,
                "message": "Login successful",
                "tokens": user.token()
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsersListApiView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer


# Follow request jo'natish
class SendFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        to_user = User.objects.get(id=request.data['to_user'])
        from_user = request.user
        follow_request = FollowRequest.objects.filter(from_user=from_user).filter(to_user=to_user)

        if not follow_request:
            try:
                FollowRequest.objects.create(from_user=from_user, to_user=to_user)
                data = {
                    "success": True,
                    "message": f"Follow request is sent to {to_user}"
                }
            except:
                data = {
                    "success": False,
                    "message": f"Follow request isn't sent!!!"
                }
        else:
            data = {
                "success": False,
                "message": "Follow request already sent"
            }

        return Response(data)


# Menga kelgan barcha follow requestlar
class MyFollowRequestsApiView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        follow_requests = FollowRequest.objects.filter(to_user=request.user, is_accepted=False)
        serializer = FollowRequestSerializer(follow_requests, many=True)

        if follow_requests:
            data = serializer.data
        else:
            data = {
                "success": False,
                "message": "You don't have any follow requests"
            }

        return Response(data)


# Kelgan follow requestni tasdiqlash
class AcceptFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        id = request.data['follow_request_id']
        try:
            follow_request_user = FollowRequest.objects.get(id=id)
            from_user = follow_request_user.from_user
            main_user = request.user

            follow_request_user.is_accepted = True
            follow_request_user.save()
            main_user.followers.add(from_user)
            from_user.followers.add(main_user)

            data = {
                "success": True,
                "message": f"{from_user.username} is accepted!"
            }
        except:
            data = {
                'success': False,
                'message': "Follow request user doesn't exist"
            }
        return Response(data)


# Followerni o'chirish
class DeleteFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, id):
        user = request.user
        follow_to_delete = get_object_or_404(user.followers, id=id)

        try:
            follow_request = FollowRequest.objects.get(from_user=follow_to_delete, to_user=user)
            follow_request.delete()
        except:
            follow_request = FollowRequest.objects.get(to_user=follow_to_delete, from_user=user)
            follow_request.delete()

        user.followers.remove(follow_to_delete)
        follow_to_delete.followers.remove(user)

        data = {
            "success": True,
            "message": f"{follow_to_delete} is deleted"
        }
        return Response(data)


# Kelgan follow reqeustni rad qilish
class IgnoreFollowRequestApiView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        id = request.data['follow_request_id']
        follow_to_ignore = get_object_or_404(FollowRequest, to_user=request.user)
        follow_to_ignore.delete()

        data = {
            "success": True,
            "message": f"{follow_to_ignore} is ignore"
        }
        return Response(data)


# Barcha followerlarni ko'rish
class MyAllFollowersListApiView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.followers.prefetch_related()




