from rest_framework import serializers
from company.models import ServiceCenterRegister
from django.contrib.auth.hashers import make_password
from users.models import MyOrder, OrderItem, OrderComplaint, OrderFeedback, UserProfile, Contact, CancelDetails

class ServiceCenterSerializer(serializers.ModelSerializer):
    # Add a confirm_password field just for validation (not saved to DB)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = ServiceCenterRegister
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password and hash the real password before saving
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        return super(ServiceCenterSerializer, self).create(validated_data)
    

# --- Service Center Profile ---
class ServiceCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCenterRegister
        fields = '__all__'

# --- Order Items (Nested in Order) ---
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

# --- Orders ---
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True) # Show items inside order

    class Meta:
        model = MyOrder
        fields = '__all__'

# --- Complaints ---
class ComplaintSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = OrderComplaint
        fields = '__all__'

# --- Cancelled Orders ---
class CancelledOrderSerializer(serializers.ModelSerializer):
    reason = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = MyOrder
        fields = '__all__'

    def get_reason(self, obj):
        # Fetch reason from CancelDetails
        cancel_obj = CancelDetails.objects.filter(order_id=obj.id).first()
        return cancel_obj.reason if cancel_obj else "No reason provided"

# --- Feedback ---
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeedback
        fields = '__all__'

# --- Customers (User Profile) ---
class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

# --- Contacts ---
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'