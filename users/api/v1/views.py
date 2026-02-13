from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from users.models import Add_Cart
from .serializers import AddCartSerializer
from decimal import Decimal
from users.models import UserProfile
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from decimal import Decimal
from rest_framework.authtoken.models import Token
from users.models import *
from .serializers import *
from users.models import Admin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from users.models import Admin
class PingAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "API working"})

class UserLoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": False,
                "errors": serializer.errors
            }, status=400)

        phone = serializer.validated_data["phone"]
        password = serializer.validated_data["password"]

        user = authenticate(username=phone, password=password)

        if not user:
            return Response({
                "status": False,
                "message": "Invalid credentials"
            }, status=401)

        token, _ = Token.objects.get_or_create(user=user)
        profile = UserProfile.objects.get(user=user)

        return Response({
            "status": True,
            "message": "Login successful",
            "token": token.key,
            "user": {
                "id": user.id,
                "fullname": profile.fullname,
                "mobile": profile.mobile,
                "email": profile.email,
                "pincode": profile.pincode
            }
        })


class CartAPI(APIView):
    permission_classes = [IsAuthenticated]

    # GET – View Cart
    def get(self, request):
        cart_items = Add_Cart.objects.filter(user=request.user)
        serializer = AddCartSerializer(cart_items, many=True)

        total_price = sum(
            item.price * item.quantity for item in cart_items
        )

        return Response({
            "items": serializer.data,
            "total_price": total_price
        })

class UserRegisterAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": False,
                "errors": serializer.errors
            }, status=400)

        data = serializer.validated_data

        if data["password"] != data["confirm_password"]:
            return Response({
                "status": False,
                "message": "Passwords do not match"
            }, status=400)

        if User.objects.filter(username=data["mobile"]).exists():
            return Response({
                "status": False,
                "message": "Mobile already registered"
            }, status=400)

        user = User.objects.create_user(
            username=data["mobile"],
            email=data["email"],
            password=data["password"]
        )

        UserProfile.objects.create(
            user=user,
            fullname=data["fullname"],
            mobile=data["mobile"],
            email=data["email"],
            state=data["state"],
            district=data["district"],
            address=data["address"],
            pincode=data["pincode"]
        )

        token = Token.objects.create(user=user)

        return Response({
            "status": True,
            "message": "Registration successful",
            "token": token.key
        }, status=201)


class UserLogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            "status": True,
            "message": "Logged out successfully"
        })


class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)

        return Response({
            "status": True,
            "data": {
                "fullname": profile.fullname,
                "mobile": profile.mobile,
                "email": profile.email,
                "state": profile.state,
                "district": profile.district,
                "address": profile.address,
                "pincode": profile.pincode
            }
        })

class RemoveFromCartAPI(APIView):
    permission_classes = [IsAuthenticated]

    # DELETE – Remove Item
    def delete(self, request, id):
        cart_item = Add_Cart.objects.get(id=id, user=request.user)
        cart_item.delete()
        return Response(
            {"message": "Item removed from cart"},
            status=status.HTTP_204_NO_CONTENT
        )
    
    
class TestAPI(APIView):
    def get(self, request):
        return Response({"msg": "API OK"})
    

class AddToCartAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        cart_item, created = Add_Cart.objects.get_or_create(
            user=request.user,
            service_name=data['service_name'],
            defaults={
                'service_details': data['service_details'],
                'details': data['details'],
                'price': Decimal(data['price']),
                'quantity': data['quantity'],
                'image': data['image'],
            }
        )

        if not created:
            cart_item.quantity += int(data['quantity'])
            cart_item.save()

        return Response(
            {"message": "Added to cart"},
            status=status.HTTP_201_CREATED
        )
class CartListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Add_Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)

        total = sum(i.price * i.quantity for i in cart_items)

        return Response({
            "items": serializer.data,
            "total_price": total
        })
class RemoveCartItemAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        item = Add_Cart.objects.get(id=item_id, user=request.user)
        item.delete()
        return Response({"message": "Item removed"})
class PlaceOrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Add_Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Cart empty"}, status=400)

        total_price = sum(i.price * i.quantity for i in cart_items)

        order = MyOrder.objects.create(
            user=user,
            fullname=request.data['fullname'],
            mobile=request.data['mobile'],
            email=request.data['email'],
            address=request.data['address'],
            district=request.data['district'],
            pincode=request.data['pincode'],
            date=request.data['date'],
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                service_name=item.service_name,
                service_details=item.service_details,
                details=item.details,
                price=item.price,
                quantity=item.quantity,
                image=item.image
            )

        cart_items.delete()

        return Response(
            {"message": "Order placed", "order_id": order.id},
            status=201
        )
class MyOrdersAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = MyOrder.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
class CancelOrderAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        if CancelDetails.objects.filter(order_id=order_id, user=request.user).exists():
            return Response({"message": "Already cancelled"}, status=400)

        CancelDetails.objects.create(
            user=request.user,
            order_id=order_id,
            reason=request.data.get("reason", "")
        )

        return Response({"message": "Order cancelled"})
class FeedbackAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = MyOrder.objects.get(id=order_id, user=request.user)

        OrderFeedback.objects.create(
            user=request.user,
            order=order,
            service_name=request.data['service_name'],
            rating=request.data['rating'],
            message=request.data['message'],
            pincode=order.pincode
        )

        return Response({"message": "Feedback submitted"})
class ComplaintAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = MyOrder.objects.get(id=order_id, user=request.user)

        OrderComplaint.objects.create(
            user=request.user,
            order=order,
            service_name=request.data['service_name'],
            complaint_text=request.data['complaint_text'],
            complaint_image=request.FILES.get("complaint_image"),
            complaint_audio=request.FILES.get("complaint_audio")
        )

        return Response({"message": "Complaint submitted"})
