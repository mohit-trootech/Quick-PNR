"""Users Urls"""

from users.api.api import RegistrationApiView
from django.urls import path, include
from rest_framework.routers import SimpleRouter

router = SimpleRouter()


(router.register("register", RegistrationApiView, basename="register"),)
urlpatterns = [
    path("", include(router.urls)),
]
