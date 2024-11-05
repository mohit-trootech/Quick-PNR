from rest_framework import mixins, viewsets, permissions
from utils.utils import get_model
from users.api.serializers import RegistrationSerializer
from users.tasks import registration_mail

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


class LoginApiView(viewsets.GenericViewSet):
    """User Login API View"""

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=self.request.data, context={"request": self.request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.get_jwt_token()

        except Exception as err:
            raise err
