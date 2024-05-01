from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, FollowRequest
from shared.utility import check_email, check_username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'phone', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

    def validate(self, validated_data):
        confirm_password = validated_data['confirm_password']
        password = validated_data['password']

        if confirm_password != password:
            data = {
                'success': False,
                'message': 'Passwords don\'t match'
            }
            raise ValidationError(data)
        if password:
            validate_password(password)
            validate_password(confirm_password)
        return validated_data

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']

        if not check_username(username):
            raise ValidationError(
                {
                    "success": False,
                    "message": "Username is not valid"
                }
            )

        if not check_email(email):
            raise ValidationError(
                {
                    "success": False,
                    "message": "Email is not valid"
                }
            )

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()
        self.validated_data['user'] = user
        return self.validated_data

    def to_representation(self, instance):
        user = instance['user']
        return user.token()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg)

        return data


class FollowRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()

    class Meta:
        model = FollowRequest
        fields = ('id', 'from_user', 'is_accepted')
        depth = 1
