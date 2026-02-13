from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from company.models import Slider, Advertisement, Advertisement1
from .serializers import (
    UserProfileSerializer, SliderSerializer,
    AdvertisementSerializer, Advertisement1Serializer)
from company.models import Product
from .serializers import ProductSerializer
from users.models import Admin
from users.models import MyOrder, CancelDetails
from users.models import UserProfile
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from users.models import Admin
from .serializers import AdminRegisterSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from users.models import Admin, UserProfile
from .serializers import AdminRegistrationSerializer
from rest_framework.permissions import IsAdminUser
from users.models import MyOrder, CancelDetails, OrderFeedback

from .serializers import (
    AdminRegistrationSerializer,
    CompanyOrderSerializer, 
    CancelDetailsSerializer, 
    OrderFeedbackSerializer
)
from company.models import (
    ACService, FanService, PressService, OvenService, TvService, 
    LaptopService, GeyserService, WashingService, WaterpurifierService, 
    WatercoolerService, FridgeService, InverterService, ChimneyService
)
# Serializers
from .serializers import (
    ACServiceSerializer, FanServiceSerializer, PressServiceSerializer, 
    OvenServiceSerializer, TvServiceSerializer, LaptopServiceSerializer, 
    GeyserServiceSerializer, WashingServiceSerializer, WaterpurifierServiceSerializer, 
    WatercoolerServiceSerializer, FridgeServiceSerializer, InverterServiceSerializer, 
    ChimneyServiceSerializer
)
from company.models import HomeService, PopularBooking, ProductBooking, SessionalBooking
from .serializers import (
    HomeServiceSerializer, PopularBookingSerializer, 
    ProductBookingSerializer, SessionalBookingSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework import status
from .serializers import ServiceCenterRegisterSerializer

# ================= 1. HOME SERVICE API =================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def homeservice_manage_api(request):
    # GET: List all services
    if request.method == 'GET':
        services = HomeService.objects.all().order_by('-created_at')
        serializer = HomeServiceSerializer(services, many=True)
        return Response(serializer.data)

    # POST: Add new service
    elif request.method == 'POST':
        serializer = HomeServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Home Service Added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def delete_homeservice_api(request, id):
    service = get_object_or_404(HomeService, id=id)
    service.delete()
    return Response({'message': 'Home Service Deleted'})


# ================= 2. POPULAR BOOKING API =================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def popularbooking_manage_api(request):
    if request.method == 'GET':
        services = PopularBooking.objects.all().order_by('-created_at')
        serializer = PopularBookingSerializer(services, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PopularBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Popular Booking Added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def update_delete_popularbooking_api(request, id):
    booking = get_object_or_404(PopularBooking, id=id)

    if request.method == 'DELETE':
        booking.delete()
        return Response({'message': 'Popular Booking Deleted'})

    elif request.method == 'PUT':
        serializer = PopularBookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Popular Booking Updated', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= 3. KITCHEN (PRODUCT BOOKING) API =================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def kitchen_manage_api(request):
    if request.method == 'GET':
        # Filter by user_id if provided, else show all
        user_id = request.GET.get('user_id')
        if user_id:
            bookings = ProductBooking.objects.filter(user_id=user_id).order_by("-created_at")
        else:
            bookings = ProductBooking.objects.all().order_by("-created_at")
            
        serializer = ProductBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Kitchen Product Added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def update_delete_kitchen_api(request, id):
    booking = get_object_or_404(ProductBooking, id=id)

    if request.method == 'DELETE':
        booking.delete()
        return Response({'message': 'Kitchen Product Deleted'})

    elif request.method == 'PUT':
        serializer = ProductBookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Kitchen Product Updated', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= 4. SESSIONAL BOOKING API =================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def sessional_manage_api(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if user_id:
            bookings = SessionalBooking.objects.filter(user_id=user_id).order_by("-created_at")
        else:
            bookings = SessionalBooking.objects.all().order_by("-created_at")
            
        serializer = SessionalBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SessionalBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sessional Booking Added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def update_delete_sessional_api(request, id):
    booking = get_object_or_404(SessionalBooking, id=id)

    if request.method == 'DELETE':
        booking.delete()
        return Response({'message': 'Sessional Booking Deleted'})

    elif request.method == 'PUT':
        serializer = SessionalBookingSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sessional Booking Updated', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    #---Services start---------
# --- HELPER FUNCTION TO HANDLE CRUD ---
def handle_service_api(request, ModelClass, SerializerClass, id=None):
    # DELETE
    if request.method == 'DELETE':
        obj = get_object_or_404(ModelClass, id=id)
        obj.delete()
        return Response({'message': 'Deleted Successfully'}, status=status.HTTP_200_OK)

    # UPDATE (PUT)
    elif request.method == 'PUT':
        obj = get_object_or_404(ModelClass, id=id)
        serializer = SerializerClass(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated Successfully', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # LIST (GET)
    elif request.method == 'GET' and id is None:
        objs = ModelClass.objects.all().order_by("-created_at")
        serializer = SerializerClass(objs, many=True)
        return Response(serializer.data)

    # CREATE (POST)
    elif request.method == 'POST':
        serializer = SerializerClass(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Created Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= SERVICE APIS =================

# 1. AC Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def ac_manage_api(request):
    return handle_service_api(request, ACService, ACServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def ac_detail_api(request, id):
    return handle_service_api(request, ACService, ACServiceSerializer, id)

# 2. Fan Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def fan_manage_api(request):
    return handle_service_api(request, FanService, FanServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def fan_detail_api(request, id):
    return handle_service_api(request, FanService, FanServiceSerializer, id)

# 3. Press Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def press_manage_api(request):
    return handle_service_api(request, PressService, PressServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def press_detail_api(request, id):
    return handle_service_api(request, PressService, PressServiceSerializer, id)

# 4. Oven Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def oven_manage_api(request):
    return handle_service_api(request, OvenService, OvenServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def oven_detail_api(request, id):
    return handle_service_api(request, OvenService, OvenServiceSerializer, id)

# 5. TV Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def tv_manage_api(request):
    return handle_service_api(request, TvService, TvServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def tv_detail_api(request, id):
    return handle_service_api(request, TvService, TvServiceSerializer, id)

# 6. Laptop Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def laptop_manage_api(request):
    return handle_service_api(request, LaptopService, LaptopServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def laptop_detail_api(request, id):
    return handle_service_api(request, LaptopService, LaptopServiceSerializer, id)

# 7. Geyser Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def geyser_manage_api(request):
    return handle_service_api(request, GeyserService, GeyserServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def geyser_detail_api(request, id):
    return handle_service_api(request, GeyserService, GeyserServiceSerializer, id)

# 8. Washing Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def washing_manage_api(request):
    return handle_service_api(request, WashingService, WashingServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def washing_detail_api(request, id):
    return handle_service_api(request, WashingService, WashingServiceSerializer, id)

# 9. Water Purifier Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def waterpurifier_manage_api(request):
    return handle_service_api(request, WaterpurifierService, WaterpurifierServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def waterpurifier_detail_api(request, id):
    return handle_service_api(request, WaterpurifierService, WaterpurifierServiceSerializer, id)

# 10. Water Cooler Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def watercooler_manage_api(request):
    return handle_service_api(request, WatercoolerService, WatercoolerServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def watercooler_detail_api(request, id):
    return handle_service_api(request, WatercoolerService, WatercoolerServiceSerializer, id)

# 11. Fridge Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def fridge_manage_api(request):
    return handle_service_api(request, FridgeService, FridgeServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def fridge_detail_api(request, id):
    return handle_service_api(request, FridgeService, FridgeServiceSerializer, id)

# 12. Inverter Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def inverter_manage_api(request):
    return handle_service_api(request, InverterService, InverterServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def inverter_detail_api(request, id):
    return handle_service_api(request, InverterService, InverterServiceSerializer, id)

# 13. Chimney Service
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def chimney_manage_api(request):
    return handle_service_api(request, ChimneyService, ChimneyServiceSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def chimney_detail_api(request, id):
    return handle_service_api(request, ChimneyService, ChimneyServiceSerializer, id)
class AdvertisementPublicListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ads = Advertisement.objects.order_by('-created_at')
        serializer = AdvertisementSerializer(
            ads, many=True, context={'request': request}
        )
        return Response({
            "status": True,
            "data": serializer.data
        })


# ================= 1. USER PROFILE API =================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def user_profile_list_api(request):
    # Fetch all profiles ordered by newest
    profiles = UserProfile.objects.all().order_by("-created_at")
    serializer = UserProfileSerializer(profiles, many=True)
    return Response(serializer.data)


# ================= 2. SLIDER API =================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def slider_manage_api(request):
    # List Sliders
    if request.method == 'GET':
        sliders = Slider.objects.all().order_by('-id')
        serializer = SliderSerializer(sliders, many=True)
        return Response(serializer.data)

    # Add Slider (Image Upload)
    elif request.method == 'POST':
        serializer = SliderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Slider Added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def delete_slider_api(request, id):
    slider = get_object_or_404(Slider, id=id)
    slider.image.delete(save=False) # Delete image file
    slider.delete()                 # Delete record
    return Response({'message': 'Slider Deleted Successfully'})


# ================= 3. ADVERTISEMENT (Main) API =================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def advertisement_manage_api(request):
    if request.method == 'GET':
        ads = Advertisement.objects.all().order_by('-created_at')
        serializer = AdvertisementSerializer(ads, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Advertisement Added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE']) # 👈 'GET' add kiya
@authentication_classes([])
@permission_classes([AllowAny])
def advertisement_update_delete_api(request, id):
    ad = get_object_or_404(Advertisement, id=id)

    # 1. Detail Dekhne ke liye (Fix for Browser)
    if request.method == 'GET':
        serializer = AdvertisementSerializer(ad)
        return Response(serializer.data)

    # 2. Delete karne ke liye
    elif request.method == 'DELETE':
        ad.image.delete(save=False)
        ad.delete()
        return Response({'message': 'Advertisement Deleted'})

    # 3. Update karne ke liye
    elif request.method == 'PUT':
        serializer = AdvertisementSerializer(ad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Advertisement Updated', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= 4. ADVERTISEMENT 1 (Second Type) API =================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def advertisement1_manage_api(request):
    if request.method == 'GET':
        ads = Advertisement1.objects.all().order_by('-created_at')
        serializer = Advertisement1Serializer(ads, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Advertisement1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Advertisement-1 Added', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def delete_advertisement1_api(request, id):
    ad = get_object_or_404(Advertisement1, id=id)
    ad.image.delete(save=False)
    ad.delete()
    return Response({'message': 'Advertisement-1 Deleted'})



# ================= SEE ALL PRODUCTS API =================

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def product_manage_api(request):
    # Reusing the helper function
    return handle_service_api(request, Product, ProductSerializer)

@api_view(['PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([AllowAny])
def product_detail_api(request, id):
    # Reusing the helper function
    return handle_service_api(request, Product, ProductSerializer, id)
# ================= 1. ADMIN REGISTRATION API =================
@api_view(['POST'])
@authentication_classes([]) # Disable Global Auth
@permission_classes([AllowAny]) # Allow Public Access
def admin_register_api(request):
    serializer = AdminRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # 1. Create Django Auth User (Main Login Table)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,      # Important: Makes them Admin
            is_superuser=False
        )

        # 2. Create Admin Profile (Your Custom Table)
        Admin.objects.create(username=username, email=email)

        return Response({
            'message': 'Admin Account Created Successfully',
            'username': username,
            'email': email
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================= 2. ADMIN LOGIN API =================
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def admin_login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({'error': 'Username and Password required'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate using Django's built-in system
    user = authenticate(username=username, password=password)

    if user is not None and user.is_staff:
        # Success
        try:
            admin_profile = Admin.objects.get(username=username)
            return Response({
                'message': 'Login Successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': 'admin'
            }, status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            return Response({'message': 'Login Successful (No Profile Found)', 'user_id': user.id}, status=status.HTTP_200_OK)
    
    else:
        return Response({'error': 'Invalid Admin Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# ================= 3. COMPANY DASHBOARD API =================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def company_dashboard_api(request):
    # Optional: You can check for 'user_id' here if you want to verify identity
    
    total_orders = MyOrder.objects.count()
    total_cancel_orders = CancelDetails.objects.count()
    total_customers = UserProfile.objects.count()

    data = {
        'total_orders': total_orders,
        'total_cancel_orders': total_cancel_orders,
        'total_customers': total_customers,
        # You can add recent orders list here later if needed
    }
    
    return Response(data, status=status.HTTP_200_OK)



##------order start--------
# ================= 1. ALL ORDERS API (With Pincode Mapping) =================
@api_view(['GET'])
@authentication_classes([])  # 👈 YE LINE ADD KI (Lock hataya)
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated]) # Or IsAdminUser
def company_orders_api(request):
    # Fetch all orders (Newest first)
    orders = MyOrder.objects.all().order_by("-created_at")
    
    # Serializer handles the logic for Items, Complaints, and Service Center mapping
    serializer = CompanyOrderSerializer(orders, many=True)
    
    return Response(serializer.data)

# ================= 2. DELETE ORDER API =================
@api_view(['GET', 'DELETE'])
@authentication_classes([]) 
@permission_classes([AllowAny])
def delete_company_order_api(request, order_id):
    order = get_object_or_404(MyOrder, id=order_id)
    order.delete()
    return Response({'message': 'Order deleted successfully'}, status=status.HTTP_200_OK)

# ================= 3. CANCELLED ORDERS API =================
@api_view(['GET'])
@authentication_classes([]) 
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def company_cancel_orders_api(request):
    # Fetch all cancel requests
    cancelled_orders = CancelDetails.objects.select_related('user').order_by('-cancelled_at')
    
    # Serializer handles fetching the linked Order Details manually
    serializer = CancelDetailsSerializer(cancelled_orders, many=True)
    
    return Response(serializer.data)

# ================= 4. REVIEWS / FEEDBACK API =================
@api_view(['GET', 'DELETE'])
@authentication_classes([]) 
@permission_classes([AllowAny])
def company_reviews_api(request):
    reviews = OrderFeedback.objects.select_related("user").order_by("-created_at")
    serializer = OrderFeedbackSerializer(reviews, many=True)
    return Response(serializer.data)

# ================= 5. DELETE FEEDBACK API =================
@api_view(['DELETE'])
@authentication_classes([]) 
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def delete_feedback_api(request, feedback_id):
    feedback = get_object_or_404(OrderFeedback, id=feedback_id)
    feedback.delete()
    return Response({'message': 'Feedback deleted successfully'}, status=status.HTTP_200_OK)




#=============Service Center Register==================3
# ================= SERVICE CENTER REGISTRATION API =================
@api_view(['POST'])
@authentication_classes([])  # Disable auth check for registration
@permission_classes([AllowAny])  # Allow anyone to register
def service_center_register_api(request):
    if request.method == 'POST':
        serializer = ServiceCenterRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Service Center Registered Successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response({
            'status': False,
            'message': 'Registration Failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)