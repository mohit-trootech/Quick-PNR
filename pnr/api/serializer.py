# PNR Serializer
from rest_framework import serializers
from utils.utils import get_model
from django.utils.timezone import timedelta

PnrDetail = get_model(app_name="pnr", model_name="PnrDetail")
PassengerDetail = get_model(app_name="pnr", model_name="PassengerDetail")


class PnrSerializer(serializers.Serializer):
    """PNR Number Serializer"""

    pnr = serializers.IntegerField()

    def validate_pnr(self, value):
        """validate pnr number"""
        if not len(str(value)) == 10:
            raise serializers.ValidationError("Invalid PNR Number")
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
        passenger_details = self.initial_data.pop("passenger_details")
        for passenger in passenger_details:
            passenger["pnr_details"] = instance.id
            serializer = PassengerDetailSerializer(data=passenger)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return instance
