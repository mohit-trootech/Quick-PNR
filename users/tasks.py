from celery import shared_task
from utils.email_service import EmailService
from utils.utils import get_model


@shared_task
def registration_mail(id: int):
    """Sends a registration email to the specified user."""
    User = get_model("users", "User")

    EmailService().registration_mail(User.objects.get(id=id))
