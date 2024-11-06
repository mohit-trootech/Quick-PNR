"""Quick PNR - Users App Constants"""

from django.utils.translation import gettext_lazy as _


class ModelFields:
    """Model Contants - QuickPnr Users"""

    INACTIVE_STATUS = 0
    ACTIVE_STATUS = 1
    STATUS_CHOICES = (
        (INACTIVE_STATUS, "Unverified"),
        (ACTIVE_STATUS, "Verified"),
    )


# Profile Thumbnail Preview
THUMBNAIL_PREVIEW_TAG = '<img src="{img}" width="320"/>'
THUMBNAIL_PREVIEW_HTML = """<div class="warning" style="color:#000;width: 320px;
        padding: 12px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: start;
        background: #FEF7D1;
        border: 1px solid #F7C752;
        border-radius: 5px;
        box-shadow: 0px 0px 5px -3px #111;">
        <div class="warning__icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" viewBox="0 0 24 24" height="24" fill="none">
                <path fill="#393a37" d="m13 14h-2v-5h2zm0 4h-2v-2h2zm-12 3h22l-11-19z" style="
        fill: #F7C752;"></path>
            </svg>
        </div>
        <strong>No Profile Image Available</strong>
    </div>"""


# User Signup Messages
class UserRegistrationMessages:
    """User Registration Constants Messages"""

    PASSWORD_DOES_NOT_MATCH = _("Password Does Not Match")
    EMAIL_EXIST_ERROR = _("Email Already Exists")
    USERNAME_ALREADY_EXISTS = _("Username Already Exists")


class AuthConstantsMessages:
    """Auth Constants Messages"""

    INVALID_EMAIL_OR_PASSWORD = _("Invalid Email or Password")
