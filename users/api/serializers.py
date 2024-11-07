from rest_framework import serializers
from utils.utils import get_model
from django.contrib.auth.password_validation import (
    validate_password as password_strength,
)
from users.contants import UserRegistrationMessages, AuthConstantsMessages, ModelFields
from django.contrib.auth import authenticate
from django.utils.timezone import now

User = get_model("users", "User")
Otp = get_model("users", "Otp")


class RegistrationSerializer(serializers.ModelSerializer):
    """
    A Simple Registration Serilizer for User Signup Process
    """

    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, password):
        """Validate Password Matches with Confirm Password"""
        password_strength(password)
        if password == self.initial_data["confirm_password"]:
            return super().validate(password)
        return serializers.ValidationError(
            UserRegistrationMessages.PASSWORD_DOES_NOT_MATCH
        )

    def create(self, validated_data):
        password = validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """User Login Serializer"""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """Validate User Credentials"""
        login_data = {
            "password": attrs.get("password"),
            "username": attrs.get("username"),
        }
        user = authenticate(**login_data)
        if not user:
            raise serializers.ValidationError(
                AuthConstantsMessages.INVALID_EMAIL_OR_PASSWORD
            )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "address",
            "image",
            "is_verified",
            "last_login",
            "date_joined",
        ]


class EmailUpdateSerializer(serializers.ModelSerializer):
    """Update User Email"""

    class Meta:
        model = User
        fields = ["email"]

    def update(self, instance, validated_data):
        """Update User Email"""
        instance.is_verified = ModelFields.INACTIVE_STATUS
        instance.save(update_fields=["is_verified"])
        return super().update(instance, validated_data)


class EmailVerifySerializer(serializers.ModelSerializer):
    """Email Verification Serializer"""

    class Meta:
        model = Otp
        fields = ["otp"]

    def validate_otp(self, value):
        """Validate OTP"""
        # Check it OTP Expired
        user = self.context["request"].user
        if user.otp.expiry < now():
            """If Expiry Date if Smaller Than Current Datetime Means OTP is Expired Hence Raise OTP Expiry Validation Error"""
            raise serializers.ValidationError(AuthConstantsMessages.OTP_EXPIRED)
        if user.otp.otp != value:
            """Check if OTP is Validated"""
            raise serializers.ValidationError(AuthConstantsMessages.INVALID_OTP)
        user.otp.delete()
        user.is_verified = ModelFields.ACTIVE_STATUS
        user.save(update_fields=["is_verified"])
        return value
