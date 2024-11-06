from rest_framework import mixins, viewsets, permissions, views, status
from rest_framework.response import Response
from utils.utils import get_model
from users.api.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)
from users.tasks import registration_mail
from utils.utils import AuthService

User = get_model("users", "User")


class RegistrationApiView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """User Registeration API View"""

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Register New User"""
        instance = super().create(request, *args, **kwargs)
        registration_mail.delay(instance.data["id"])
        return instance


class LoginApiView(views.APIView):
    """User Login API View"""

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=self.request.data, context={"request": self.request}
            )
            serializer.is_valid(raise_exception=True)
            return Response(
                AuthService().get_auth_tokens_for_user(serializer.validated_data),
                status=status.HTTP_200_OK,
            )
        except BaseException as err:
            raise Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        """Return User Object"""
        return self.request.user

    def get(self, *args, **kwargs):
        """Return User Profile"""
        try:
            instance = self.get_object(*args, **kwargs)
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        except BaseException as err:
            raise Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """Update User Profile"""
        try:
            instance = self.get_object()
            serializer = self.serializer_class(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except BaseException as err:
            raise Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)
