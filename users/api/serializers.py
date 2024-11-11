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
        return value

    def update(self, instance, validated_data):
        """Update User Email"""
        instance.otp.delete()
        instance.is_verified = ModelFields.ACTIVE_STATUS
        instance.save(update_fields=["is_verified"])
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[password_strength])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        """Validation Password Validation"""
        user = self.context["request"].user
        old_password = attrs["old_password"]
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": ["Wrong Password"]})
        if old_password == new_password:
            raise serializers.ValidationError(
                {"new_password": ["New Password Should Not Be Same As Old Password"]}
            )

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": ["Password Does Not Match"]}
            )
        return attrs

    def update(self, instance, validated_data):
        """Update User Password"""
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.IntegerField(required=False)
    # new_password = serializers.CharField(required=False, validators=[password_strength])
    new_password = serializers.CharField(required=False)
    confirm_password = serializers.CharField(required=False)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(["User with this email does not exist"])
        return value

    def validate_otp(self, value):
        """Validate OTP"""
        user = User.objects.get(email=self.initial_data["email"])
        if user.otp.expiry < now():
            raise serializers.ValidationError(AuthConstantsMessages.OTP_EXPIRED)
        if user.otp.otp != value:
            raise serializers.ValidationError(AuthConstantsMessages.INVALID_OTP)
        return value

    def validate(self, attrs):
        """Validation Password Validation"""
        attrs = super().validate(attrs)
        if "otp" not in attrs:
            return attrs
        new_password = attrs["new_password"]
        confirm_password = attrs["confirm_password"]
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": ["Password Does Not Match"]}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance
