from rest_framework import viewsets
from utils.utils import get_model
from users.api.serializers import RegistrationSerializer

User = get_model("user", "User")


class RegistrationApiView(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
