from rest_framework import serializers
from .models import Restaurant, Table, TablesRestaurant, Product, ProductsRestaurant, Waiter, Order, ProductsOrder, Bill, TipWaiter, WaiterShift, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class TablesRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TablesRestaurant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductsRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsRestaurant
        fields = '__all__'

class WaiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiter
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ProductsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOrder
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

class TipWaiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipWaiter
        fields = '__all__'

class WaiterShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiterShift
        fields = '__all__'