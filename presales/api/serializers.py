from rest_framework import serializers
from management.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresalesMember
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    members = MemberSerializer(read_only=True, many=True)
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Activity
        fields = '__all__'