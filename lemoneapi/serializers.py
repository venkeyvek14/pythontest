from rest_framework import serializers
from .models import Users, SystemSpec

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'user_name', 'email']

class SystemSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSpec
        fields = ['system_spec_id', 'user_id', 'created_at', 'system_info', 'deleted_at', 'status']
