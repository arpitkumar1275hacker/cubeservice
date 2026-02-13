from django.urls import path
from . import views


urlpatterns = [
    # --- 1. Home Service ---
    path('homeservice/', views.homeservice_manage_api, name='api_homeservice'),
    path('homeservice/delete/<int:id>/', views.delete_homeservice_api, name='api_delete_homeservice'),

    # --- 2. Popular Booking ---
    path('popular-bookings/', views.popularbooking_manage_api, name='api_popularbooking'),
    path('popular-bookings/update/<int:id>/', views.update_delete_popularbooking_api, name='api_update_popular'),

    # --- 3. Kitchen (Product Booking) ---
    path('kitchen/', views.kitchen_manage_api, name='api_kitchen'),
    path('kitchen/update/<int:id>/', views.update_delete_kitchen_api, name='api_update_kitchen'),

    # --- 4. Sessional Booking ---
    path('sessional/', views.sessional_manage_api, name='api_sessional'),
    path('sessional/update/<int:id>/', views.update_delete_sessional_api, name='api_update_sessional'),
# ================= APPLIANCES SERVICES (UPDATED) =================
    # Ab hum naye 'manage_api' aur 'detail_api' use karenge

    # 1. AC
    path('ac/', views.ac_manage_api, name='api_ac_manage'),
    path('ac/<int:id>/', views.ac_detail_api, name='api_ac_detail'),

    # 2. Fan
    path('fan/', views.fan_manage_api, name='api_fan_manage'),
    path('fan/<int:id>/', views.fan_detail_api, name='api_fan_detail'),

    # 3. Press
    path('press/', views.press_manage_api, name='api_press_manage'),
    path('press/<int:id>/', views.press_detail_api, name='api_press_detail'),

    # 4. Oven
    path('oven/', views.oven_manage_api, name='api_oven_manage'),
    path('oven/<int:id>/', views.oven_detail_api, name='api_oven_detail'),

    # 5. TV
    path('tv/', views.tv_manage_api, name='api_tv_manage'),
    path('tv/<int:id>/', views.tv_detail_api, name='api_tv_detail'),

    # 6. Laptop
    path('laptop/', views.laptop_manage_api, name='api_laptop_manage'),
    path('laptop/<int:id>/', views.laptop_detail_api, name='api_laptop_detail'),

    # 7. Geyser
    path('geyser/', views.geyser_manage_api, name='api_geyser_manage'),
    path('geyser/<int:id>/', views.geyser_detail_api, name='api_geyser_detail'),

    # 8. Washing Machine
    path('washing/', views.washing_manage_api, name='api_washing_manage'),
    path('washing/<int:id>/', views.washing_detail_api, name='api_washing_detail'),

    # 9. Water Purifier
    path('waterpurifier/', views.waterpurifier_manage_api, name='api_waterpurifier_manage'),
    path('waterpurifier/<int:id>/', views.waterpurifier_detail_api, name='api_waterpurifier_detail'),

    # 10. Water Cooler
    path('watercooler/', views.watercooler_manage_api, name='api_watercooler_manage'),
    path('watercooler/<int:id>/', views.watercooler_detail_api, name='api_watercooler_detail'),

    # 11. Fridge
    path('fridge/', views.fridge_manage_api, name='api_fridge_manage'),
    path('fridge/<int:id>/', views.fridge_detail_api, name='api_fridge_detail'),

    # 12. Inverter
    path('inverter/', views.inverter_manage_api, name='api_inverter_manage'),
    path('inverter/<int:id>/', views.inverter_detail_api, name='api_inverter_detail'),

    # 13. Chimney
    path('chimney/', views.chimney_manage_api, name='api_chimney_manage'),
    path('chimney/<int:id>/', views.chimney_detail_api, name='api_chimney_detail'),

    # 1. User Profiles
    path('user-profiles/', views.user_profile_list_api, name='api_user_profiles'),

    # 2. Sliders
    path('slider/', views.slider_manage_api, name='api_slider_manage'),
    path('slider/delete/<int:id>/', views.delete_slider_api, name='api_slider_delete'),

    # 3. Advertisement (Main)
    path('advertisement/', views.advertisement_manage_api, name='api_ad_manage'),
    path('advertisement/<int:id>/', views.advertisement_update_delete_api, name='api_ad_update_delete'),

    # 4. Advertisement 1 (Type 2)
    path('advertisement1/', views.advertisement1_manage_api, name='api_ad1_manage'),
    path('advertisement1/delete/<int:id>/', views.delete_advertisement1_api, name='api_ad1_delete'),

    # Public (User App)
    
    # Company (Admin)
    # See All Products (Shop)
    path('see-all-products/', views.product_manage_api, name='api_product_manage'),
    path('see-all-products/<int:id>/', views.product_detail_api, name='api_product_detail'),
    path('register/', views.admin_register_api, name='api_admin_register'),
    path('login/', views.admin_login_api, name='api_admin_login'),
    path('dashboard/', views.company_dashboard_api, name='api_company_dashboard'),
    # ... existing admin login/register urls ...

    # Order Management
    path('orders/', views.company_orders_api, name='api_company_orders'),
    path('orders/delete/<int:order_id>/', views.delete_company_order_api, name='api_delete_order'),

    # Cancelled Orders
    path('orders/cancelled/', views.company_cancel_orders_api, name='api_cancel_orders'),

    # Feedback / Reviews
    path('reviews/', views.company_reviews_api, name='api_company_reviews'),
    path('reviews/delete/<int:feedback_id>/', views.delete_feedback_api, name='api_delete_review'),

    path('api/service-center/register/', views.service_center_register_api, name='api_service_center_register'),
]























































