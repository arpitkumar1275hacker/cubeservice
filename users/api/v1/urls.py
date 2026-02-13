from django.urls import path
from .views import (
    PingAPI,
    TestAPI,

    UserLoginAPI,
    UserRegisterAPI,
    UserLogoutAPI,
    UserProfileAPI,

    AddToCartAPI,
    CartListAPI,
    RemoveCartItemAPI,

    PlaceOrderAPI,
    MyOrdersAPI,
    CancelOrderAPI,

    FeedbackAPI,
    ComplaintAPI,
)


urlpatterns = [

    
    # 🧪 Test
    path("ping/", PingAPI.as_view()),
    path("test/", TestAPI.as_view()),
    
     # 🔐 Auth
    path("login/", UserLoginAPI.as_view()),
    path("register/", UserRegisterAPI.as_view()),
    path("logout/", UserLogoutAPI.as_view()),
    path("profile/", UserProfileAPI.as_view()),

    
    # 🛒 Cart
    path("cart/", CartListAPI.as_view()),              # GET
    path("cart/add/", AddToCartAPI.as_view()),         # POST
    path("cart/remove/<int:item_id>/", RemoveCartItemAPI.as_view()),  # DELETE

    # 📦 Orders
    path("order/place/", PlaceOrderAPI.as_view()),     # POST
    path("orders/", MyOrdersAPI.as_view()),            # GET
    path("order/cancel/<int:order_id>/", CancelOrderAPI.as_view()),

    # ⭐ Feedback & Complaint
    path("feedback/<int:order_id>/", FeedbackAPI.as_view()),
    path("complaint/<int:order_id>/", ComplaintAPI.as_view()),


    path("login/", UserLoginAPI.as_view()),
    path("register/", UserRegisterAPI.as_view()),
    path("logout/", UserLogoutAPI.as_view()),
    path("profile/", UserProfileAPI.as_view()),



]
