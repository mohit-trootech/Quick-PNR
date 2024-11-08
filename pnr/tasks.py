from celery import shared_task
from utils.email_service import EmailService
from utils.utils import get_model
from pnr.api.serializer import PnrDetailSerializer
from pnr.constants import MessageConstants

User = get_model("users", "User")
PnrDetail = get_model("pnr", "PnrDetail")
EmailService = EmailService()


@shared_task
def send_pnr_details(user_id, pnr_id):
    """Send PNR Details to User"""
    user = User.objects.get(id=user_id)
    pnr = PnrDetail.objects.get(id=pnr_id)
    serializer = PnrDetailSerializer(pnr)
    EmailService.pnr_status_mail(user, serializer.data)
    return MessageConstants.PNR_DETAILS_MAILED
