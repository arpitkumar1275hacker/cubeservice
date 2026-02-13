from rest_framework import serializers
from company.models import HomeService, PopularBooking, ProductBooking, SessionalBooking
from company.models import (
    ACService, FanService, PressService, OvenService, TvService, 
    LaptopService, GeyserService, WashingService, WaterpurifierService, 
    WatercoolerService, FridgeService, InverterService, ChimneyService)
from users.models import UserProfile
from company.models import Slider, Advertisement, Advertisement1
from company.models import Product
from users.models import Admin
from django.contrib.auth.models import User
from users.models import MyOrder, OrderItem, CancelDetails, OrderFeedback, OrderComplaint
from company.models import ServiceCenterRegister
from django.contrib.auth.hashers import make_password



# --- 1. Home Service ---
class HomeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeService
        fields = '__all__'

# --- 2. Popular Booking ---
class PopularBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularBooking
        fields = '__all__'

# --- 3. Kitchen (Product Booking) ---
class ProductBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBooking
        fields = '__all__'

# --- 4. Sessional Booking ---
class SessionalBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionalBooking
        fields = '__all__'

# 1. AC Service
class ACServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACService
        fields = '__all__'

# 2. Fan Service
class FanServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FanService
        fields = '__all__'

# 3. Press Service
class PressServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressService
        fields = '__all__'

# 4. Oven Service
class OvenServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OvenService
        fields = '__all__'

# 5. TV Service
class TvServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvService
        fields = '__all__'

# 6. Laptop Service
class LaptopServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaptopService
        fields = '__all__'

# 7. Geyser Service
class GeyserServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeyserService
        fields = '__all__'

# 8. Washing Machine Service
class WashingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashingService
        fields = '__all__'

# 9. Water Purifier Service
class WaterpurifierServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterpurifierService
        fields = '__all__'

# 10. Water Cooler Service
class WatercoolerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatercoolerService
        fields = '__all__'

# 11. Fridge Service
class FridgeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeService
        fields = '__all__'

# 12. Inverter Service
class InverterServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InverterService
        fields = '__all__'

# 13. Chimney Service
class ChimneyServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChimneyService
        fields = '__all__'


    
# --- 1. User Profile Serializer ---
class UserProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

# --- 2. Slider Serializer ---
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'

# --- 3. Advertisement Serializer ---
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'

# --- 4. Advertisement1 Serializer ---
class Advertisement1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement1
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
class AdminRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class AdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
            
        return data
    ## --- Company order start-------
# --- 1. Feedback Serializer ---
class OrderFeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = OrderFeedback
        fields = '__all__'

# --- 2. Complaint Serializer ---
class OrderComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderComplaint
        fields = '__all__'

# --- 3. Order Item Serializer ---
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

# --- 4. Service Center Serializer (Helper) ---

class ServiceCenterRegisterSerializer(serializers.ModelSerializer):
    # Add a confirm_password field purely for validation (not saved to DB)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = ServiceCenterRegister
        fields = [
            'username', 'servicecenter_name', 'author_name', 
            'district', 'state', 'pincode', 'aadhaar', 
            'mobile', 'email', 'password', 'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'aadhaar': {'required': True},
            'mobile': {'required': True},
        }

    def validate(self, data):
        # 1. Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        # 2. Check if Username exists (DRF does this usually, but good to be explicit if needed)
        # Note: 'unique=True' in model handles Username, Email, Aadhaar, Mobile automatically.
        
        return data

    def create(self, validated_data):
        # Remove confirm_password before saving
        validated_data.pop('confirm_password')
        
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])
        
        # Create and return the instance
        return ServiceCenterRegister.objects.create(**validated_data)







class ServiceCenterSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCenterRegister
        fields = ['id', 'servicecenter_name', 'district', 'mobile', 'pincode']















# --- 5. Main Order Serializer ---
class CompanyOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    complaints = serializers.SerializerMethodField()
    assigned_service_center = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MyOrder
        fields = '__all__'

    def get_complaints(self, obj):
        # Fetch complaints related to this order
        complaints = OrderComplaint.objects.filter(order=obj)
        return OrderComplaintSerializer(complaints, many=True).data

    def get_assigned_service_center(self, obj):
        # Logic: Find Service Center that matches the Order's Pincode
        try:
            sc = ServiceCenterRegister.objects.filter(pincode=obj.pincode).first()
            if sc:
                return ServiceCenterSimpleSerializer(sc).data
        except:
            pass
        return None

# --- 6. Cancelled Order Serializer ---
class CancelDetailsSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CancelDetails
        fields = '__all__'

    def get_order_details(self, obj):
        # Logic: Fetch the actual Order object using the integer order_id
        try:
            order = MyOrder.objects.get(id=obj.order_id)
            return CompanyOrderSerializer(order).data
        except MyOrder.DoesNotExist:
            return None