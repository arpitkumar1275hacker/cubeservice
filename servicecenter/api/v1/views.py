from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password

# Models
from company.models import ServiceCenterRegister
from users.models import MyOrder, OrderComplaint, OrderFeedback, UserProfile, Contact, CancelDetails

# Serializers
from .serializers import (
    ServiceCenterSerializer, OrderSerializer, ComplaintSerializer, 
    FeedbackSerializer, CustomerSerializer, ContactSerializer, CancelledOrderSerializer
)

# --- Helper Function ---
def get_service_center(request):
    user_id = request.GET.get('user_id') or request.data.get('user_id')
    if not user_id:
        return None
    try:
        return ServiceCenterRegister.objects.get(id=user_id)
    except ServiceCenterRegister.DoesNotExist:
        return None

# ================= 1. AUTHENTICATION (Register & Login) =================

@api_view(['POST'])
@authentication_classes([])  # 👈 YE IMPORTANT HAI (Auth Disable)
@permission_classes([AllowAny]) # 👈 YE IMPORTANT HAI (Public Access)
def register_servicecenter_api(request):
    if ServiceCenterRegister.objects.filter(username=request.data.get('username')).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ServiceCenterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Registered Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_servicecenter_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = ServiceCenterRegister.objects.get(username=username)
        if check_password(password, user.password):
            return Response({
                'message': 'Login Successful',
                'user_id': user.id,
                'username': user.username,
                'district': user.district,
                'pincode': user.pincode
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
    except ServiceCenterRegister.DoesNotExist:
        return Response({'error': 'Username not found'}, status=status.HTTP_404_NOT_FOUND)

# ================= 2. DASHBOARD & PROFILE =================

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def servicecenter_dashboard_api(request):
    servicecenter = get_service_center(request)
    if not servicecenter:
        return Response({'error': 'User ID required'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ServiceCenterSerializer(servicecenter)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@authentication_classes([])
@permission_classes([AllowAny])
def servicecenter_profile_api(request):
    servicecenter = get_service_center(request)
    if not servicecenter:
        return Response({'error': 'Service Center ID required'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = ServiceCenterSerializer(servicecenter)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ServiceCenterSerializer(servicecenter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile Updated', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= 3. ORDERS & COMPLAINTS =================

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def servicecenter_orders_api(request):
    servicecenter = get_service_center(request)
    if not servicecenter:
        return Response({'error': 'Service Center ID required'}, status=status.HTTP_400_BAD_REQUEST)

    district = servicecenter.district
    pincode = servicecenter.pincode

    orders = MyOrder.objects.filter(district__iexact=district, pincode=pincode).order_by("-created_at")
    
    complaints = OrderComplaint.objects.filter(
        user__userprofile__district__iexact=district,
        user__userprofile__pincode=pincode
    ).order_by("-created_at")

    data = {
        "orders": OrderSerializer(orders, many=True).data,
        "complaints": ComplaintSerializer(complaints, many=True).data,
        "counts": {
            "total": orders.count(),
            "accepted": orders.filter(status="accepted").count(),
            "rejected": orders.filter(status="rejected").count(),
            "pending": orders.filter(status="pending").count(),
        }
    }
    return Response(data)

# ================= 4. ORDER ACTIONS (Accept/Reject) =================

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def update_order_status_api(request, order_id):
    servicecenter = get_service_center(request)
    if not servicecenter:
        return Response({'error': 'Service Center ID required'}, status=status.HTTP_400_BAD_REQUEST)

    action = request.data.get('action') 
    
    try:
        order = MyOrder.objects.get(id=order_id, status="pending")
    except MyOrder.DoesNotExist:
        return Response({'error': 'Order not found or not pending'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'accept':
        order.status = "accepted"
        order.service_center_id = servicecenter.id
        order.save()
        return Response({'message': 'Order Accepted Successfully'})
    
    elif action == 'reject':
        order.status = "rejected"
        order.save()
        return Response({'message': 'Order Rejected'})

    return Response({'error': 'Invalid Action'}, status=status.HTTP_400_BAD_REQUEST)

# ================= 5. CANCELLED ORDERS =================

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def service_cancel_orders_api(request):
    servicecenter = get_service_center(request)
    if not servicecenter:
        return Response({'error': 'Service Center ID required'}, status=status.HTTP_400_BAD_REQUEST)

    cancelled_ids = CancelDetails.objects.values_list("order_id", flat=True)
    cancelled_orders = MyOrder.objects.filter(
        id__in=cancelled_ids, 
        pincode=servicecenter.pincode
    ).order_by("-created_at")

    serializer = CancelledOrderSerializer(cancelled_orders, many=True)
    return Response(serializer.data)

# ================= 6. CUSTOMERS LIST =================

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def customers_list_api(request):
    servicecenter = get_service_center(request)
    if not servicecenter:
        return Response({'error': 'Service Center ID required'}, status=status.HTTP_400_BAD_REQUEST)

    customers = UserProfile.objects.filter(pincode=servicecenter.pincode)
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# ================= 7. FEEDBACK & CONTACTS =================

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def feedback_contacts_api(request):
    servicecenter = get_service_center(request)
    if not servicecenter:
        return Response({'error': 'Service Center ID required'}, status=status.HTTP_400_BAD_REQUEST)

    feedbacks = OrderFeedback.objects.filter(pincode=servicecenter.pincode).order_by('-created_at')
    contacts = Contact.objects.filter(pincode=servicecenter.pincode).order_by("-created_at")

    data = {
        "feedbacks": FeedbackSerializer(feedbacks, many=True).data,
        "contacts": ContactSerializer(contacts, many=True).data
    }
    return Response(data)