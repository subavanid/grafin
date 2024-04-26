from rest_framework import serializers
from .models import *


class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['room','added_by']


class HomeApplianceserializer(serializers.ModelSerializer):
    class Meta:
        model = HomeAppliance
        fields = '__all__'


class Officeserializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['officeroom','added_by']


class OfficeApplianceserializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeAppliance
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email', 'password']