from rest_framework import serializers
from exam.models.order import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'categories', 'total_price', 'start_day', 'end_day']

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        # Create the Order instance
        order = Order.objects.create(**validated_data)

        order.categories.set(categories)

        price = sum(category.price for category in categories)
        order.total_price = price
        order.save(update_fields=['total_price'])

        return order