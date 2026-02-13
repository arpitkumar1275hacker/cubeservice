from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import Admin
from .models import OrderItem ,MyOrder
from django.contrib.auth import authenticate, login as auth_login
from company.models import HomeService
from company.models import PopularBooking
from company.models import SessionalBooking
from company.models import ProductBooking
from company.models import ACService , GeyserService
from company.models import  GeyserService
from company.models import FanService
from company.models import PressService
from company.models import WaterpurifierService
from company.models import OvenService
from company.models import TvService
from company.models import InverterService
from company.models import ChimneyService
from company.models import WatercoolerService
from company.models import LaptopService
from company.models import WashingService
from company.models import ServiceCenterRegister
from django.shortcuts import redirect, get_object_or_404
from .models import CancelDetails
import datetime
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from .models import Add_Cart
from django.views.decorators.csrf import csrf_exempt
from .models import OrderFeedback, OrderComplaint
from django.db.models import Avg
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now
from company.models import Product
from company.models import Slider
from company.models import Advertisement 
from company.models import Advertisement1
from django.contrib.auth.hashers import make_password, check_password
from company.models import Policy
from .models import Contact 
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
import random
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db import IntegrityError



def index(request):
    return render(request, "index.html")
def home(request):
    services = HomeService.objects.all().order_by("-created_at")
    popular_services = PopularBooking.objects.order_by("-created_at")[:10]
    product_services = ProductBooking.objects.order_by("-created_at")[:10]
    sessional_services = SessionalBooking.objects.order_by("-created_at")[:10]
    sliders = Slider.objects.all().order_by('-id')
    ads = Advertisement.objects.all().order_by('-created_at')
    ads1 = Advertisement1.objects.all().order_by('-created_at')



    return render(request, "home.html", {
        "services": services,
         "product_services": product_services,
         "popular_services": popular_services,
         "sessional_services": sessional_services,  
          "sliders": sliders,
          "ads": ads,
          "ads1": ads1,

        
    })







@csrf_exempt
def user_login(request):
    if request.method == "POST":
        phone = request.POST.get("phone", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            user_obj = User.objects.get(username=phone)
        except User.DoesNotExist:
            messages.error(request, "Mobile number not registered")
            return redirect("users:home")

        user = authenticate(request, username=user_obj.username, password=password)

        if user:
            login(request, user)

            profile = UserProfile.objects.get(user=user)
            request.session["user_mobile"] = profile.mobile
            request.session["user_pincode"] = profile.pincode
            request.session["login_time"] = str(datetime.datetime.now())

            return redirect("users:home")

        messages.error(request, "Invalid password")
        return redirect("users:home")

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect("users:forgot_password")

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri(
            reverse("users:reset_password", args=[uid, token])
        )

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link below to reset your password:\n\n{reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Password reset link sent to your email")
        return redirect("users:forgot_password")

    return render(request, "forgot_password.html")
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect(request.path)

            user.set_password(password)
            user.save()

            messages.success(request, "Password reset successful. Please login.")
            return redirect("users:index")

        return render(request, "reset_password.html")

    messages.error(request, "Invalid or expired reset link")
    return redirect("users:forgot_password")


def register(request):
    if request.method == "POST":

        fullname = request.POST.get("fullname")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password != cpassword:
            return render(request, "home.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=mobile).exists():
            if User.objects.filter(email=email).exists():
              return render(request, "index.html", {
             "error": "Email already registered"
    })

            return render(request, "home.html", {
                "error": "Mobile already registered"
            })

        # Create user
        user = User.objects.create_user(
        username=mobile,
        email=email,          # ✅ MUST
        password=password
)


        # Create user profile
        UserProfile.objects.create(
            user=user,
            fullname=fullname,
            mobile=mobile,
            email=email,
            state=state,
            district=district,
            address=address,
            pincode=pincode
        )

        login(request, user)

        # Session create
        request.session["user_mobile"] = mobile
        request.session["user_pincode"] = pincode
        request.session["login_time"] = str(datetime.datetime.now())

        return redirect("users:home")

    return redirect("users:home")
def save_activity(request, activity):
    activity_list = request.session.get("activity_log", [])
    activity_list.append(activity)
    request.session["activity_log"] = activity_list



@login_required(login_url="home")
def user_panel(request):
    return render(request, "user_panel.html")
def order_success(request):
    return render(request, "order_success.html")

def user_logout(request):
    logout(request)
    request.session.flush()   # delete all session data
    return redirect("users:home")




# ================= Admin REGISTER =================
def adminreg(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("users:adminreg")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("users:adminreg")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("users:adminreg")

        # Create Django auth user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            is_staff=True,         # make admin
            is_superuser=False     # or True if you want full superuser rights
               # or True if you want full superuser rights
        )

        # Create Admin profile
        Admin.objects.create(
            username=username,
            email=email
        )

        messages.success(request, "Admin account created successfully")
        return redirect("users:admin_login")

    return render(request, "adminreg.html")

# ================= Admin LOGIN =================#

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            auth_login(request, user)
            return redirect("company:compdashboard")  # Admin dashboard

        messages.error(request, "Invalid admin credentials")
        return redirect("users:admin_login")

    return render(request, "admin_login.html")


#=================Ac Service Views ==================#
def ac(request):
    services = ACService.objects.all().order_by('-id')

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "ac.html", {
        "services": services,
        "cart_count": cart_count,
        
    })
#=============Geyser Service=========#
def geyser(request):
    services = GeyserService.objects.all().order_by('-id')

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "geyser.html", {
        "services": services,
        "cart_count": cart_count,
        
    })
def fan(request):
    services = FanService.objects.all().order_by("-id")

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "fan.html", {
        "services": services,
         "cart_count": cart_count,
    })

def tv(request):
    services = TvService.objects.all().order_by("-id")

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")
    return render(request, 'tv.html', {'services': services,
                                        "cart_count": cart_count,})





def fridge(request):
    services = PressService.objects.all().order_by('-id')

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "fridge.html", {
        "services": services,
         "cart_count": cart_count,
    })



def press(request):
    services = PressService.objects.all().order_by('-id')

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "press.html", {
        "services": services,
         "cart_count": cart_count,
    })



def oven(request):
    services = OvenService.objects.all().order_by('-id')

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "oven.html", {
        "services": services,
        "cart_count": cart_count,
    })


def cart(request):
    
    return render(request, "cart.html")


def inverter(request):
    services = InverterService.objects.all().order_by("-created_at")
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "inverter.html", {
        "services": services,
         "cart_count": cart_count,
    })



def chimney(request):
    services = ChimneyService.objects.all().order_by("-created_at")
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "chimney.html", {
        "services": services,
         "cart_count": cart_count,
    })

def laptop(request):
    services = LaptopService.objects.all().order_by("-created_at")
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "laptop.html", {
        "services": services,
         "cart_count": cart_count,
    })

#==============Washing Machine Service================#
def washing(request):
    services = WashingService.objects.all().order_by("-created_at")
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "washing.html", {
        "services": services,
         "cart_count": cart_count,
    })

#==============Water Purifier Service================#
def waterpurifier(request):
    services = WaterpurifierService.objects.all().order_by("-created_at")
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "waterpurifier.html", {
        "services": services,
         "cart_count": cart_count,
    })

#==============Water Cooler Service================#


def watercooler(request):
    services = WatercoolerService.objects.all().order_by("-created_at")
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Add_Cart.objects.filter(user=request.user).count()

        
    for service in services:
        service.feedbacks = OrderFeedback.objects.filter(
            service_name=service.product_name
        ).order_by("-created_at")

    return render(request, "watercooler.html", {
        "services": services,
         "cart_count": cart_count,
    })

       
 # redirect to login if not authenticated
def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first to add items to cart.")
        return redirect('users:index')
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        service_details = request.POST.get("service_details")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")
        price = Decimal(request.POST.get("price"))
        quantity = int(request.POST.get("quantity"))
        image = request.POST.get("image")

        user = request.user

        cart_item, created = Add_Cart.objects.get_or_create(
            user=user,
            service_name=service_name,
            defaults={
                "price": price,
                "service_details":service_details,
                "details":details,
                "extra_details":extra_details,
                "quantity": quantity,
                "image": image,
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f"{service_name} added to cart successfully!")
        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("users:oven")
def cart(request):
    user = request.user if request.user.is_authenticated else None
    
    if user is None:
        cart_items = []  # or redirect to login
    else:
        cart_items = Add_Cart.objects.filter(user=user)

    # Calculate total price
    total_price = sum(item.price * item.quantity for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "cart.html", context)

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Add_Cart, id=item_id)
    cart_item.delete()
    return redirect('users:cart')  # 



@login_required
def create_order(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    cart_items = Add_Cart.objects.filter(user=user)
    total_price = sum(item.price * item.quantity for item in cart_items)

    if request.method == "POST":

        # 1️⃣ Save Profile
        if "save_profile" in request.POST:
            profile.fullname = request.POST.get("fullname")
            profile.mobile = request.POST.get("mobile")
            profile.email = request.POST.get("email")
            profile.address = request.POST.get("address")
            profile.district = request.POST.get("district")
            profile.pincode = request.POST.get("pincode")
            profile.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("users:create_order")

        # 2️⃣ Place Order
        elif "place_order" in request.POST:

            service_names = request.POST.getlist("service_name[]")
            service_details = request.POST.getlist("service_details[]")
            details = request.POST.getlist("details[]")
            extra_details = request.POST.getlist("extra_details[]")
            prices = request.POST.getlist("price[]")
            quantities = request.POST.getlist("quantity[]")
            images = request.POST.getlist("image[]")

            if not service_names:
                messages.warning(request, "Cart is empty, cannot place order.")
                return redirect("users:cart")

            order = MyOrder.objects.create(
                user=user,
                fullname=request.POST.get("fullname"),
                mobile=request.POST.get("mobile"),
                email=request.POST.get("email"),
                address=request.POST.get("address"),
                district=request.POST.get("district"),
                pincode=request.POST.get("pincode"),
                date=request.POST.get("date"),
                total_price=total_price
            )

            order_summary = ""

            for i in range(len(service_names)):
                OrderItem.objects.create(
                    order=order,
                    service_name=service_names[i],
                    service_details=service_details[i],
                    details=details[i],
                    extra_details=extra_details[i],
                    price=Decimal(prices[i]),
                    quantity=int(quantities[i]),
                    image=images[i]
                )

                order_summary += f"- {service_names[i]} (Qty: {quantities[i]}) ₹{prices[i]}\n"

            html_message = render_to_string("emails/order_email_template.html", {
                "name": order.fullname,
                "order_id": order.id,
                "service_date": order.date,
                "address": order.address,
                "district": order.district,
                "pincode": order.pincode,
                "order_summary": order_summary,
                "total_price": total_price,
                "year": now().year,
            })

            send_mail(
                subject="CUBEService – Order Confirmation",
                message=strip_tags(html_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                html_message=html_message,
                fail_silently=False,
            )

            cart_items.delete()
            messages.success(request, "Order placed successfully!")
            return redirect("users:order_success")

    # ✅ THIS IS THE MISSING PART (FOR GET REQUEST)
    return render(request, "create_order.html", {
        "profile": profile,
        "cart_items": cart_items,
        "total_price": total_price,
    })

@login_required
def place_order(request):
    if request.method == "POST":

        fullname = request.POST.get("fullname")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        address = request.POST.get("address")
        district = request.POST.get("district")
        pincode = request.POST.get("pincode")
        total_price = request.POST.get("total_price")
        date = request.POST.get("date")
        time = request.POST.get("time")  # New field for time

        service_names = request.POST.getlist("service_name[]")
        service_details = request.POST.getlist("service_details[]")
        details = request.POST.getlist("details[]")
        extra_details = request.POST.getlist("extra_details[]")
        prices = request.POST.getlist("price[]")
        quantities = request.POST.getlist("quantity[]")
        images = request.POST.getlist("image[]")

        for i in range(len(service_names)):
            MyOrder.objects.create(
                user=request.user,
                fullname=fullname,
                mobile=mobile,
                email=email,
                address=address,
                district=district,
                pincode=pincode,
                date=date,
                service_name=service_names[i],
                service_details=service_details[i],
                details=details[i],
                extra_details=extra_details[i],
                price=prices[i],
                quantity=quantities[i],
                image=images[i],
                total_price=total_price
            )

        messages.success(request, "Order placed successfully!")
        return redirect("my_orders")

    return redirect("cart")
@login_required
def my_orders(request):
    orders = MyOrder.objects.filter(user=request.user).order_by("-created_at")
    cancel_qs = CancelDetails.objects.filter(user=request.user)
    cancel_orders = {c.order_id: c for c in cancel_qs}

    return render(request, 'my_orders.html', {
        'orders': orders,
        'cancel_orders': cancel_orders
    })
   


@login_required
def cancel_order(request, order_id):

    # 🔒 Duplicate cancel रोकना
    if CancelDetails.objects.filter(order_id=order_id, user=request.user).exists():
        messages.info(request, "Order already cancelled.")
        return redirect('users:my_orders')

    if request.method == 'POST':
        reason = request.POST.get('reason', '')

        # Order fetch (optional but useful)
        order = get_object_or_404(MyOrder, id=order_id, user=request.user)

        # ❌ Save cancel details
        CancelDetails.objects.create(
            user=request.user,
            order_id=order_id,
            reason=reason
        )

        # 📧 Email message
        email_message = f"""
Hello {order.fullname},

Your order has been successfully CANCELLED ❌

📦 Order ID: {order.id}
💰 Order Amount: ₹{order.total_price}

📝 Cancellation Reason:
{reason if reason else 'Not specified'}

If this was a mistake or you need help, please contact our support team.

Thank you,
CUBEService Team
"""

        # 📤 Send Email
        send_mail(
            subject="CUBEService – Order Cancelled Confirmation",
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )

        messages.success(request, "Order cancelled successfully. Confirmation email sent.")

    return redirect('users:my_orders')
@login_required
@login_required
def submit_feedback(request, order_id):
    if request.method == "POST":

        order = get_object_or_404(
            MyOrder,
            id=order_id,
            user=request.user
        )

        OrderFeedback.objects.create(
            user=request.user,
            order=order,                     # ✅ FIX
            service_name=request.POST.get("service_name"),
            rating=int(request.POST.get("rating")),
            message=request.POST.get("message"),
            pincode=order.pincode            # ✅ FIX
        )

        messages.success(request, "Thanks for your feedback!")

    return redirect("users:my_orders")

@login_required
def submit_complaint(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(MyOrder, id=order_id, user=request.user)

        OrderComplaint.objects.create(
            user=request.user, 
            order=order,
            service_name=request.POST.get("service_name"),  # ✅ add this
            complaint_text=request.POST.get("complaint_text"),
            complaint_image=request.FILES.get("complaint_image"),  # ✅ NEW
            complaint_audio=request.FILES.get("complaint_audio")
        )

        messages.success(request, "Complaint submitted successfully.")
        return redirect("users:my_orders")


#===========See All Product================#
def all_services(request):
    query = request.GET.get('q')

    products = Product.objects.all().order_by('-created_at')

    if query:
        products = products.filter(
            productName__icontains=query
        ) | products.filter(
            serviceDetails__icontains=query
        )

    context = {
        'products': products,
        'query': query
    }
    return render(request, 'all_services.html', context)


def login_servicecenter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = ServiceCenterRegister.objects.get(username=username)

            if check_password(password, user.password):
                request.session['servicecenter_id'] = user.id
                request.session['username'] = user.username
                request.session['pincode'] = user.pincode
                request.session['district'] = user.district

                return redirect('servicecenter:servicecenterdashboard')  # must exist in urls.py

            else:
                messages.error(request, 'Invalid password')

        except ServiceCenterRegister.DoesNotExist:
            messages.error(request, 'Username not found')

    return render(request, 'login_servicecenter.html')


def about_us(request):
    return render(request, "about_us.html")

def policy(request):
    policy = Policy.objects.first()

    return render(request, "policy.html", {
        "policy": policy
    })




@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "fullname": request.user.get_full_name(),
            "email": request.user.email
        }
    )

    if request.method == "POST":
        profile.fullname = request.POST.get("fullname")
        profile.mobile = request.POST.get("mobile")
        profile.email = request.POST.get("email")
        profile.state = request.POST.get("state")
        profile.district = request.POST.get("district")
        profile.address = request.POST.get("address")
        profile.pincode = request.POST.get("pincode")
        profile.save()

        return redirect("users:user_profile")

    return render(request, "user_profile.html", {
        "profile": profile
    })


@login_required
@login_required
def update_user_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        new_mobile = request.POST.get("mobile", "").strip()

        # 🔒 Check duplicate mobile
        if User.objects.exclude(id=request.user.id).filter(username=new_mobile).exists():
            messages.error(request, "This mobile number is already in use.")
            return redirect("users:update_user_profile")

        # ✅ UPDATE BOTH MODELS
        request.user.username = new_mobile
        request.user.save()

        profile.fullname = request.POST.get("fullname")
        profile.mobile = new_mobile
        profile.email = request.POST.get("email")
        profile.state = request.POST.get("state")
        profile.district = request.POST.get("district")
        profile.address = request.POST.get("address")
        profile.pincode = request.POST.get("pincode")

        profile.save()

        # 🔐 IMPORTANT: keep session valid
        update_session_auth_hash(request, request.user)

        messages.success(request, "Profile updated successfully!")
        return redirect("users:update_user_profile")

    return render(request, "user_profile.html", {
        "profile": profile
    })
@login_required
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("users:change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("users:change_password")

        user.set_password(new_password)
        user.save()

        # 🔥 MUST
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully. Please login again.")
        logout(request)   # 🔒 Force clean login
        return redirect("users:index")

    return render(request, "change_password.html")

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            mobile=request.POST.get("mobile"),
            email=request.POST.get("email"),
            pincode=request.POST.get("pincode"),  # ✅ SAVE
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("users:contact")

    return render(request, "contact.html")



    

def investor_relations(request):
    return render(request, "investor_relations.html")




def esg_impact(request):
    return render(request, "esg_impact.html")