from rest_framework import serializers
from utils.utils import get_model
from django.contrib.auth.password_validation import validate_password
from users.contants import UserRegistrationMessages

User = get_model("user", "User")


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
        extra_kwargs = {
            "password": {"write_only": True},
            "validators": [validate_password],
        }

    def validate_password(self, password):
        """Validate Password Matches with Confirm Password"""
        if password == self.initial_data["confirm_password"]:
            return super().validate(password)
        return serializers.ValidationError(
            UserRegistrationMessages.PASSWORD_DOES_NOT_MATCH
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
