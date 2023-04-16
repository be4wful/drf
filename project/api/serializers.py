from rest_framework import serializers

from .models import User, Product, Cart, Order

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fio', 'email', 'password']

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['fio'],
            fio=self.validated_data['fio'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'