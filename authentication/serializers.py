from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

from authentication.models import User


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, min_length=3, write_only=True)
    password = serializers.CharField(max_length=100, write_only=True, min_length=4)
    token = serializers.SerializerMethodField(method_name="get_user_token")

    class Meta:
        model = User
        fields = ['password', 'username', 'token']

    def validate(self, attrs):
        request = self.context["request"]
        super().validate(attrs)
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        if username is None and password is None:
            raise AuthenticationFailed('Invalid credentials, try again')
        user = authenticate(request, username=username, password=password)
        if not user or not user.is_active:
            raise AuthenticationFailed('Invalid credentials, try again')
        response_data = user.token()
        return response_data

    def get_user_token(self, obj):
        return obj


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "confirm_password")

    def validate(self, attrs):
        if User.objects.filter(username__iexact=attrs["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Already Exists!"}
            )
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=False, validators=[UniqueValidator(queryset=User.objects.all())], min_length=3
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "date_joined"]

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
