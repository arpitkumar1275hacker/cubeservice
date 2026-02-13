from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile
from users.models import Add_Cart
from rest_framework import serializers
from users.models import (
    Add_Cart, MyOrder, OrderItem,
    OrderFeedback, OrderComplaint, CancelDetails
)
from users.models import Admin


class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    mobile = serializers.CharField()
    email = serializers.EmailField()
    state = serializers.CharField()
    district = serializers.CharField()
    address = serializers.CharField()
    pincode = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)




class AddCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_Cart
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_Cart
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = MyOrder
        fields = '__all__'
class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelDetails
        fields = '__all__'
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeedback
        fields = '__all__'
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderComplaint
        fields = '__all__'
class AdminRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("Username already exists")
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        return data