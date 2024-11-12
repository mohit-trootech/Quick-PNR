from celery import shared_task
from utils.email_service import EmailService
from utils.utils import get_model
from pnr.api.serializer import PnrDetailSerializer
from pnr.constants import ReponseMessages

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
    return ReponseMessages.PNR_DETAILS_MAILED


@shared_task
def multiple_pnr_found(pnr):
    """Reduce Multiple PNR to one only"""
    # Only Excluce Last Modified PNR
    PnrDetail.objects.filter(
        pk__in=PnrDetail.objects.filter(pnr=pnr).order_by("-modified")[1:]
    ).delete()
    return ReponseMessages.MULTIPLE_PNR_FOUND_ERROR_HANDLED.format(pnr=pnr)
