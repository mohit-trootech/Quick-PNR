"""Mail Services"""

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from utils.utils import get_model
from django_extensions.db.models import ActivatorModel
from utils.constants import EmailTemplates

EmailTemplate = get_model("quickpnr", "EmailTemplate")
Otp = get_model(app_name="users", model_name="Otp")


class EmailService:
    """Email Service Class to Handle Mail"""

    @staticmethod
    def get_template(self, email_type: str):
        """Returns Email Template"""
        try:
            EmailTemplate.objects.get(
                status=ActivatorModel.ACTIVE_STATUS, email_type=email_type
            )
        except EmailTemplate.DoesNotExist:
            return None

    @staticmethod
    def send_mail(
        subject: str,
        body: str,
        template: str | None,
        is_html: bool,
        to_email: list,
    ):
        """This function will be used to send email using celery task based on email template"""
        sender = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(
            subject=subject, from_email=sender, to=[to_email], body=body
        )
        if is_html:
            msg.attach_alternative(template, "text/html")
        msg.send()
        return

    def registration_mail(self, user):
        """Sends a registration email to the specified user."""
        template = self.get_template(email_type=EmailTemplates.REGISTRED_SUCCESSFULLY)
        self.send_email(
            template.subject,
            template.body,
            template.template,
            template.is_html,
            [user.email],
        )

    def verify_email(self, user):
        """Send a Verification email to Specific User"""
        from django.utils.timezone import now, timedelta

        template = self.get_template(email_type=EmailTemplates.VERIFY_EMAIL)
        otp, created = Otp.objects.get_or_create(
            user=user, expiry=now() + timedelta(minutes=10)
        )
        self.send_mail(
            template.subject,
            template.body,
            template.template.format(otp=otp.otp, expiry=otp.expiry),
            template.is_html,
            [user.email],
        )
