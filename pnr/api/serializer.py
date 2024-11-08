# PNR Serializer
from rest_framework import serializers
from utils.utils import get_model
from django.utils.timezone import timedelta
from utils.exceptions import InvalidPnrNumber
from pnr.constants import MessageConstants

PnrDetail = get_model(app_name="pnr", model_name="PnrDetail")
PassengerDetail = get_model(app_name="pnr", model_name="PassengerDetail")


class PnrSerializer(serializers.Serializer):
    """PNR Number Serializer"""

    pnr = serializers.IntegerField()

    def validate_pnr(self, value):
        """validate pnr number"""
        if not len(str(value)) == 10:
            raise InvalidPnrNumber(MessageConstants.INVALID_PNR)
        return value


class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ["id", "name", "booking_status", "current_status", "pnr_details"]
        extra_kwargs = {"pnr_details": {"write_only": True}}


class PnrDetailSerializer(serializers.ModelSerializer):
    passengers_details = PassengerDetailSerializer(many=True, read_only=True)

    class Meta:
        model = PnrDetail
        fields = [
            "id",
            "pnr",
            "train_number",
            "train_name",
            "boarding_date",
            "boarding_point",
            "reserved_from",
            "reserved_to",
            "reserved_class",
            "fare",
            "remark",
            "status",
            "modified",
            "train_status",
            "charting_status",
            "passengers_details",
        ]
        depth = 1

    def create(self, validated_data):
        validated_data["expiry"] = validated_data["boarding_date"] + timedelta(days=5)
        instance = super().create(validated_data)
        # Create Passenger Details Instances using Serializer
        passengers_details = self.initial_data.pop("passengers_details")
        for passenger in passengers_details:
            passenger["pnr_details"] = instance.id
            serializer = PassengerDetailSerializer(data=passenger)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance=instance, validated_data=validated_data)
        # Update Passenger Details Instances using Serializer
        passengers_details = self.initial_data.pop("passengers_details")
        for passenger in passengers_details:
            passenger["pnr_details"] = instance.id
            # Update Passenger Details
            try:
                obj = PassengerDetail.objects.get(
                    name=passenger["name"], pnr_details=instance.id
                )
                serializer = PassengerDetailSerializer(
                    obj, data=passenger, partial=True
                )
            except PassengerDetail.DoesNotExist:
                serializer = PassengerDetailSerializer(data=passenger)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        breakpoint()
        return super().update(instance, validated_data)
