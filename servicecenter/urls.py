from django.urls import path
from . import views
from .views import service_cancel_orders

# servicecenter/urls.py
app_name = 'servicecenter'


urlpatterns = [
    path('servicecenterdashboard/', views.servicecenterdashboard, name='servicecenterdashboard'),  # /touristadminapp/ → index view
    path('servicecenter_profile/', views.servicecenter_profile, name='servicecenter_profile'),
    path('edit_servicecenter_profile/', views.edit_servicecenter_profile, name='edit_servicecenter_profile'),   
    path('servicecenter_orders/', views.servicecenter_orders, name='servicecenter_orders'),
     path("service_cancel_orders/", service_cancel_orders, name="service_cancel_orders"),
        path("servicecenter/orders/accept/<int:order_id>/", views.accept_order, name="accept_order"),
    path("servicecenter/orders/reject/<int:order_id>/", views.reject_order, name="reject_order"),
     path(
        "feedbacks/",
        views.servicecenter_feedback,
        name="servicecenter_feedback"
    ),
    path("logout/", views.servicecenter_logout, name="servicecenter_logout"),
    path('customers_list/', views.customers_list, name='customers_list'),
    path('servicecenter_contacts/', views.servicecenter_contacts, name='servicecenter_contacts'),
    
  


]