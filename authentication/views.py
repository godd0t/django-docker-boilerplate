from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from authentication.serializers import LoginSerializer, RegisterSerializer, ProfileSerializer


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_id="User Login")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={
            "request": request
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="User Registration")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(operation_id="Get User Profile")
    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(operation_id="Update User Profile")
    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
