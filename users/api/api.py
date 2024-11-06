from rest_framework import mixins, viewsets, permissions, views, status
from rest_framework.response import Response
from utils.utils import get_model
from users.api.serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
    EmailUpdateSerializer,
    EmailVerifySerializer,
)
from users.tasks import registration_mail, generate_otp
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
        serializer = self.serializer_class(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            AuthService().get_auth_tokens_for_user(serializer.validated_data),
            status=status.HTTP_200_OK,
        )


class UserProfileView(views.APIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        """Return User Object"""
        return self.request.user

    def get(self, *args, **kwargs):
        """Return User Profile"""
        instance = self.get_object(*args, **kwargs)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Update User Profile"""
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class EmailUpdateView(views.APIView):
    """User Email Update View"""

    serializer_class = EmailUpdateSerializer

    def patch(self, *args, **kwargs):
        """Update User Email"""
        serializer = self.serializer_class(
            self.request.user, data=self.request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailVerifyView(views.APIView):
    """Email Verification API View"""

    serializer_class = EmailVerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Send Email Verification OTP"""
        generate_otp.delay(request.user.id)
        try:
            return Response(
                {"message": "OTP Sent Successfully"}, status=status.HTTP_200_OK
            )
        except Exception as err:
            raise Response(
                {
                    "message": f"Failed to send OTP, {err}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, *args, **kwargs):
        """Verify User Email"""
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Email Verified Successfully"},
            status=status.HTTP_200_OK,
        )
