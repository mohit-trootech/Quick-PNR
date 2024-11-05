from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from users.contants import (
    ModelFields,
    THUMBNAIL_PREVIEW_TAG,
    THUMBNAIL_PREVIEW_HTML,
)
from django.utils.html import format_html
from django_extensions.db.models import TimeStampedModel


def _upload_to(self, filename):
    """Upload User Profile Image"""
    return "users/{id}/{filename}".format(id=self.id, filename=filename)


class User(AbstractUser):
    """Abstract User Model"""

    image = models.ImageField(upload_to=_upload_to, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    is_verified = models.IntegerField(
        _("verification status"),
        choices=ModelFields.STATUS_CHOICES,
        default=ModelFields.INACTIVE_STATUS,
    )
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    @property
    def profile_image(self):
        """Profile Image Viewer"""
        if self.image:
            return format_html(THUMBNAIL_PREVIEW_TAG.format(img=self.image.url))
        return format_html(THUMBNAIL_PREVIEW_HTML)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy("user:details", kwargs={"username": self.username})


class Otp(TimeStampedModel):
    """OTP Models to Store OTP Details"""

    otp = models.IntegerField()
    expiry = models.DateTimeField()
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="otp"
    )

    def __str__(self):
        return "{user}'s OTP".format(user=self.user.username)

    def save(self, *args, **kwargs):
        from random import randint

        self.otp = randint(100000, 999999)
        return super(Otp, self).save(*args, **kwargs)
