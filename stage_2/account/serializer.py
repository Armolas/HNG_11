from rest_framework import serializers
from .models import User, Organisation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "firstName", "lastName", "phone", "password"]
        extra_kwargs = {
                'password': {'write_only': True},
                'phone': {'required': False}
                }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["userId", "firstName", "lastName", "email", "phone"]

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ["name", "description"]
        extra_kwargs = {
                'description': {'required': False}
                }
    
    def create(self, validated_data):
        return Organisation.objects.create(**validated_data)

class OrgResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']
