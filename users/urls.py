from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("panel/", views.user_panel, name="user_panel"),
    path("logout/", views.user_logout, name="logout"),
    path('admin_login/', views.admin_login, name='admin_login'),
   
    path('adminreg/', views.adminreg, name='adminreg'),
    
    path("ac/", views.ac, name="ac"),
    path("fan/", views.fan, name="fan"),
    path("tv/", views.tv, name="tv"),
    path("oven/", views.oven, name="oven"),
     path("geyser/", views.geyser, name="geyser"),
    path("fridge/", views.fridge, name="fridge"),
    path("press/", views.press, name="press"),
    path("cart/add/", views.cart, name="cart"),
    path("add_to_cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
     path("laptop/", views.laptop, name="laptop"),
     path("washing/", views.washing, name="washing"),
     path("waterpurifier/", views.waterpurifier, name="waterpurifier"),
    path("watercooler/", views.watercooler, name="watercooler"),
    
    path("inverter/", views.inverter, name="inverter"),
    path("chimney/", views.chimney, name="chimney"),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("create-order/", views.create_order, name="create_order"),
    #path('update-profile/', views.update_profile, name='update_profile'),
    path("place-order/", views.place_order, name="place_order"),
     path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
     path('order_success/', views.order_success, name='order_success'),
     # urls.py
    path("feedback/<int:order_id>/", views.submit_feedback, name="submit_feedback"),
    path('submit_complaint/<int:order_id>/', views.submit_complaint, name='submit_complaint'),
    path('all_services/', views.all_services, name='all_services'),
    path('login_servicecenter/', views.login_servicecenter, name='login_servicecenter'),
    path("about_us/", views.about_us, name="about_us"),
    path("policy/", views.policy, name="policy"),  # ✅ POLICY URL
    path("contact/", views.contact, name="contact"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset_password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("update_user_profile/", views.update_user_profile, name="update_user_profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("investors/", views.investor_relations, name="investor_relations"),
    path("esg_impact/", views.esg_impact, name="esg_impact"),
]