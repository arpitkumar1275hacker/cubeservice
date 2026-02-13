from django.urls import path
from . import views

urlpatterns = [
    # ... your existing urls ...
    
    # API URLs
    path('register/', views.register_servicecenter_api, name='api_service_register'),
    path('login/', views.login_servicecenter_api, name='api_service_login'),
    path('dashboard/', views.servicecenter_dashboard_api, name='api_service_dashboard'),
    # Profile
    path('profile/', views.servicecenter_profile_api, name='api_service_profile'), # GET to view, PUT to edit

    # Orders & Actions
    path('orders/', views.servicecenter_orders_api, name='api_service_orders'), # Lists Orders & Complaints
    path('orders/update/<int:order_id>/', views.update_order_status_api, name='api_update_order'), # Accept/Reject
    path('orders/cancelled/', views.service_cancel_orders_api, name='api_cancelled_orders'),

    # Users & Data
    path('customers/', views.customers_list_api, name='api_customers'),
    path('data/', views.feedback_contacts_api, name='api_feedback_contacts'), # Feedbacks + Contacts
]