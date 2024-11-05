from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Abstract User Model"""

    def __str__(self):
        return self.title
