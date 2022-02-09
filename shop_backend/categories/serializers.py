from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for products categories.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']
