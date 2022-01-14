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
        fields = ['id', 'price', 'quantity', 'status']


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
    positions = BasketPositionSerializer(read_only=True, many=True, required=False, source='contents')
    total = serializers.SerializerMethodField('get_total', required=False)

    class Meta:
        model = Order
        fields = ['id', 'total', 'status', 'positions']

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
            new_user_order = Order.objects.create(status='new', user=request_user)

            for basket_position in basket_contents:
                # Creating a new user order with the same content as in the basket
                basket_position.id = None
                basket_position.order_id = new_user_order.id
                basket_position.save()

                # Splitting the new user order into multiple unique sub-orders for the suppliers
                supplier = basket_position.product_info.shop.user
                new_supplier_order, created = Order.objects.get_or_create(parent_order_id=new_user_order.id,
                                                                          status='new',
                                                                          user=supplier)
                OrderContent.objects.create(product_info=basket_position.product_info, order=new_supplier_order,
                                            quantity=basket_position.quantity)

            basket_contents.delete()

        return new_user_order

    def update(self, instance, validated_data):
        status = validated_data.get('status')

        if not status:
            raise ValidationError({'results': ['Provide a status for the order.']})

        with transaction.atomic():
            instance.status = status
            instance.save()

            supplier_order_positions = instance.contents.all()
            for supplier_position in supplier_order_positions:
                supplier_position.status = status
                supplier_position.save()
            else:
                supplier = supplier_position.product_info.shop.user

            parent_order = Order.objects.get(id=instance.parent_order_id)
            parent_order_positions = parent_order.contents.filter(product_info__shop__user=supplier)
            for parent_position in parent_order_positions:
                parent_position.status = status
                parent_position.save()

        return instance
