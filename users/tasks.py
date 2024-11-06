from celery import shared_task
from utils.email_service import EmailService
from utils.utils import get_model

User = get_model("users", "User")


@shared_task
def registration_mail(id: int):
    """Sends a registration email to the specified user."""

    return EmailService().registration_mail(User.objects.get(id=id))


@shared_task
def generate_otp(id: int):
    """Sends a verification email to the specified user."""

    return EmailService().verify_email(User.objects.get(id=id))
