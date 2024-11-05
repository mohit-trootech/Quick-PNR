"""Users Urls"""

from django.urls import path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

app_name = "user"
urlpatterns = [path("/")]
