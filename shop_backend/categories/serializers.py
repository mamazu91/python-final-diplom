from rest_framework import serializers
from .models import Category


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for products categories.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']
