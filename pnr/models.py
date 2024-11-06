# Pnr Scrapping Details Model
from django.db import models
from pnr.constants import ModelsConstants, ModelVerbose


class PnrDetails:
    """Store PNR Details"""

    train_number = models.IntegerField(verbose_name=ModelVerbose.TRAIN_NUMBER)
    train_name = models.CharField(max_length=132, verbose_name=ModelVerbose.TRAIN_NAME)
    boarding_date = models.DateField(verbose_name=ModelVerbose.BOARDING_DATE)
    reserved_from = models.CharField(verbose_name=ModelVerbose.RESERVED_FROM)
    reserved_to = models.CharField(verbose_name=ModelVerbose.RESERVED_TO)
    reserved_class = models.CharField(verbose_name=ModelVerbose.RESERVED_CLASS)
    fare = models.DecimalField(
        decimal_places=2, max_digits=10, verbose_name=ModelVerbose.FARE
    )
    remark = models.CharField(verbose_name=ModelVerbose.REMARK)
    train_status = models.CharField(verbose_name=ModelVerbose.TRAIN_STATUS)


class PassengerDetails:
    """Store Passenger Details"""

    pnr_details = models.ForeignKey(
        "pnr.PnrDetails",
        on_delete=models.CASCADE,
        related_name=ModelsConstants.PNR_DETAILS,
    )
    name = models.CharField(verbose_name=ModelVerbose.NAME)
    booking_status = models.CharField(verbose_name=ModelVerbose.BOOKING_STATUS)
    current_status = models.CharField(verbose_name=ModelVerbose.CURRENT_STATUS)
