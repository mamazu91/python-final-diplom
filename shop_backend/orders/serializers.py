from rest_framework import serializers
from orders.models import Order, OrderContent
from products.models import ProductInfo
from rest_framework.exceptions import ValidationError
from django.db.models import F, Sum
from django.db import transaction


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'created_at']


class BasketPositionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product_info.id')
    price = serializers.SlugRelatedField(read_only=True, slug_field='price', source='product_info')

    class Meta:
        model = OrderContent
        fields = ['id', 'price', 'quantity']


class BasketSerializer(serializers.ModelSerializer):
    positions = BasketPositionSerializer(many=True, source='contents')
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = Order
        fields = ['id', 'total', 'positions']

    @staticmethod
    def get_total(obj):
        order_total = Order.objects.filter(id=obj.id).aggregate(
            total=(Sum(F('contents__quantity') * F('positions__price'))))
        return order_total['total']

    def update(self, instance, validated_data):
        basket_positions = validated_data.pop('contents')
        if not basket_positions:
            raise ValidationError({'results': ['You need to add at least one position to basket.']})

        for basket_position in basket_positions:
            basket_position_id = basket_position.get('product_info').get('id')
            basket_position_quantity = basket_position.get('quantity')
            position_in_stock = ProductInfo.objects.get(id=basket_position_id)

            if basket_position.get('quantity') > position_in_stock.quantity:
                raise ValidationError(
                    {'results': [f'Cannot add {basket_position_quantity} items of position {basket_position_id}. '
                                 f'Only {position_in_stock.quantity} is in stock.']})

            OrderContent.objects.update_or_create(
                order=instance,
                product_info=position_in_stock,
                defaults={'quantity': basket_position_quantity}
            )
            instance.save()

        return instance


class UserOrderSerializer(serializers.ModelSerializer):
    positions = BasketPositionSerializer(read_only=True, many=True, source='contents')
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = Order
        fields = ['id', 'total', 'positions']

    @staticmethod
    def get_total(obj):
        order_total = Order.objects.filter(id=obj.id).aggregate(
            total=(Sum(F('contents__quantity') * F('positions__price'))))
        return order_total['total']

    def create(self, validated_data):
        request_user = self.context['request'].user
        basket = Order.objects.get(user=request_user, status='basket')

        with transaction.atomic():
            basket_contents = basket.contents.all()
            new_order = Order.objects.create(status='new', user=request_user)

            for basket_content in basket_contents:
                basket_content.id = None
                basket_content.order_id = new_order.id
                basket_content.save()

            basket_contents.delete()

        return new_order


class OrderContentSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(read_only=True, slug_field='product_id', source='product_info')
    name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='product_info.product')
    price = serializers.SlugRelatedField(read_only=True, slug_field='price', source='product_info')

    class Meta:
        model = OrderContent
        fields = ['id', 'name', 'quantity', 'price']


class OrderItemsSerializer(BasketSerializer):
    items = OrderContentSerializer(many=True, allow_null=True, source='contents')
    total = serializers.ReadOnlyField()

    class Meta(BasketSerializer.Meta):
        fields = BasketSerializer.Meta.fields + ['total', 'items']
