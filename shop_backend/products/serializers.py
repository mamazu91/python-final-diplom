from rest_framework import serializers
from .models import Product, ProductInfo


class ProductSerializer(serializers.ModelSerializer):
    """
    Base product serializer that exposes only those fields that every product must have.
    To add some other fields, inherit from this serializer.
    """
    class Meta:
        model = Product
        fields = ['id', 'name']


class ProductInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for products details.
    """
    position_id = serializers.IntegerField(source='id')
    shop_id = serializers.SlugRelatedField(read_only=True, slug_field='id', source='shop')
    shop = serializers.SlugRelatedField(read_only=True, slug_field='name')
    category_id = serializers.SlugRelatedField(read_only=True, slug_field='id', source='product.category')
    category = serializers.SlugRelatedField(read_only=True, slug_field='name', source='product.category')
    in_stock = serializers.IntegerField(source='quantity')

    class Meta:
        model = ProductInfo
        fields = ['position_id', 'shop_id', 'shop', 'category_id', 'category', 'in_stock', 'price']


class ProductDetailsSerializer(ProductSerializer):
    """
    Serializer for products and details on its availability in shops.
    """
    available_in = ProductInfoSerializer(many=True, allow_null=True, source='infos')

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['available_in']
