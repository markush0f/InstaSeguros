from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "birth"]

class ValidationUserSerializer(Exception):
    def __init__(self, errors):
        super().__init__("Validation failed")
        self.errors = errors
