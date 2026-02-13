from django.shortcuts import render
from .models import HomeService
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from .models import PopularBooking
from .models import ProductBooking
from .models import SessionalBooking
from .models import ACService 
from .models import WaterpurifierService
from .models import WashingService
from .models import  GeyserService
from .models import FanService
from .models import FridgeService
from .models import PressService
from .models import OvenService
from .models import TvService
from .models import LaptopService
from .models import WatercoolerService
from .models import InverterService
from .models import ChimneyService
from users.models import OrderFeedback
from users.models import CancelDetails
from django.contrib.admin.views.decorators import staff_member_required
from users.models import MyOrder, OrderItem, CancelDetails , OrderComplaint 
from .models import Product
from users.models import UserProfile
from .models import Slider
from .models import Advertisement
from .models import Advertisement1
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password, check_password
from .models import ServiceCenterRegister
from .models import Policy
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

@login_required(login_url='users:admin_login')
def compdashboard(request):
    total_orders = MyOrder.objects.count()
    total_cancel_orders = CancelDetails.objects.count()
    total_customer = UserProfile.objects.count()

    context = {
        'total_orders': total_orders,
        'total_cancel_orders': total_cancel_orders,
        'total_customer': total_customer,
    }
    return render(request, 'compdashboard.html', context)

@login_required(login_url='users:admin_login')
def homeservice(request):

    if request.method == "POST":
        productName = request.POST.get("productName")
        productImage = request.FILES.get("productImage")

        if not productName or not productImage:
            messages.error(request, "All fields are required")
            return redirect("company:homeservice")

        HomeService.objects.create(
            user=request.user,
            productName=productName,
            productImage=productImage
        )

        messages.success(request, "Home Service added successfully")
        return redirect("company:homeservice")

    # ✔ Correct placement (return के ऊपर)
    services = HomeService.objects.filter(user=request.user).order_by('-created_at')

    # ✔ services context के साथ return
    return render(request, "homeservice.html", {"services": services})

@login_required(login_url='users:admin_login')
def delete_homeservice(request, id):
    service = get_object_or_404(HomeService, id=id, user=request.user)

    if request.method == "POST":
        service.delete()
        messages.success(request, "Home Service deleted successfully")

    return redirect("company:homeservice")

@login_required(login_url='users:admin_login')
def popularbooking(request):
    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_image = request.FILES.get("productImage")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")

        if not product_name or not product_image:
            messages.error(request, "Product name and image are required!")
            return redirect(request.path)

        # Save to database
        booking = PopularBooking(
            product_name=product_name,
            product_image=product_image,
            service_details=service_details,
            rating=int(rating) if rating else 0,
            price=price,
            link=link
        )
        booking.save()
        messages.success(request, "✔ Successfully Submitted")
        return redirect("company:popularbooking")

    services = PopularBooking.objects.all().order_by('-created_at')
    return render(request, "popularbooking.html", {"services": services})
@login_required
def delete_popularbooking(request, id):
    booking = get_object_or_404(PopularBooking, id=id)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
    return redirect("company:popularbooking")




@login_required
def update_popularbooking(request, id):
    booking = get_object_or_404(PopularBooking, id=id)

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = int(request.POST.get("rating"))
        booking.price = request.POST.get("price")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        messages.success(request, "Popular booking updated successfully")
        return redirect("company:popularbooking")

    return render(request, "popularbooking.html", {
        "booking": booking,
        "is_update": True,
        "services": PopularBooking.objects.all().order_by('-created_at')
    })
@login_required
def kitchen(request):

    bookings = ProductBooking.objects.filter(
        user=request.user
    ).order_by("-created_at")

    if request.method == "POST":
        productName = request.POST.get("productName")
        productImage = request.FILES.get("productImage")
        serviceDetails = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")

        if not all([productName, productImage, serviceDetails, rating, price, link]):
            messages.error(request, "All fields are required")
            return redirect("company:kitchen")

        ProductBooking.objects.create(
            user=request.user,
            productName=productName,
            productImage=productImage,
            serviceDetails=serviceDetails,
            rating=rating,
            price=price,
            link=link
        )

        messages.success(request, "Product Booking added successfully")
        return redirect("company:kitchen")

    return render(request, "kitchen.html", {
        "bookings": bookings
    })
@login_required
def update_kitchen(request, id):
    booking = get_object_or_404(ProductBooking, id=id)

    if request.method == "POST":
        booking.productName = request.POST.get("productName")
        booking.serviceDetails = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.link = request.POST.get("link")  # IMPORTANT FIX

        if request.FILES.get("productImage"):
            booking.productImage = request.FILES.get("productImage")

        booking.save()
        messages.success(request, "Product booking updated successfully")
        return redirect("company:kitchen")

    return render(request, "kitchen.html", {
        "booking": booking,
        "is_update": True
    })


@login_required
def delete_kitchen(request, id):
    booking = get_object_or_404(ProductBooking, id=id)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Product booking deleted successfully")

    return redirect("company:kitchen")

# =================  SESSIONAL BOOKING =================
@login_required
def sessionalbooking(request):

    bookings = SessionalBooking.objects.filter(
        user=request.user
    ).order_by("-created_at")

    if request.method == "POST":
        productName = request.POST.get("productName")
        productImage = request.FILES.get("productImage")
        serviceDetails = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")

        if not all([productName, productImage, serviceDetails, rating, price, link]):
            messages.error(request, "All fields are required")
            return redirect("company:sessionalbooking")  # ✔ FIXED URL

        SessionalBooking.objects.create(
            user=request.user,
            productName=productName,
            productImage=productImage,
            serviceDetails=serviceDetails,
            rating=rating,
            price=price,
            link=link
        )

        messages.success(request, "Sessional Booking added successfully")
        return redirect("company:sessionalbooking")

    return render(request, "sessionalbooking.html", {
        "bookings": bookings
    })
@login_required
def delete_sessionalbooking(request, id):
    booking = get_object_or_404(SessionalBooking, id=id, user=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Sessional booking deleted successfully")

    return redirect("company:sessionalbooking")
@login_required
def update_sessionalbooking(request, id):

    booking = get_object_or_404(SessionalBooking, id=id, user=request.user)

    if request.method == "POST":
        booking.productName = request.POST.get("productName")
        booking.serviceDetails = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.link = request.POST.get("link")

        if request.FILES.get("productImage"):
            booking.productImage = request.FILES.get("productImage")

        booking.save()
        messages.success(request, "Sessional Booking updated successfully")
        return redirect("company:sessionalbooking")

    return render(request, "sessionalbooking.html", {
        "booking": booking,
        "is_update": True,
        "bookings": SessionalBooking.objects.filter(user=request.user).order_by("-created_at")
    })



#==========ac service ======================#
def ac_service(request, id=None):

    if id:
        booking = ACService.objects.get(id=id)
        is_update = True
    else:
        booking = None
        is_update = False

    if request.method == "POST":

        productName = request.POST.get("productName")
        serviceDetails = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")
        productImage = request.FILES.get("productImage")

        if is_update:
            booking.product_name = productName
            booking.service_details = serviceDetails
            booking.rating = rating
            booking.price = price
            booking.link = link
            booking.details = details
            booking.extra_details = extra_details

            if productImage:
                booking.product_image = productImage

            booking.save()

        else:
            ACService.objects.create(
                product_name=productName,
                product_image=productImage,
                service_details=serviceDetails,
                rating=rating,
                price=price,
                link=link,
                details=details,
                extra_details=extra_details
            )

        return redirect("company:ac_service")

    services = ACService.objects.all().order_by("-id")

    return render(request, "ac_service.html", {
        "services": services,
        "is_update": is_update,
        "booking": booking
    })
def delete_ac_service(request, id):
    booking = ACService.objects.get(id=id)
    booking.delete()
    return redirect("company:ac_service")



#===================== Fan Service Views =====================#

@login_required(login_url='users:admin_login')
def fan_service(request):
    services = FanService.objects.all().order_by("-id")

    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_image = request.FILES.get("productImage")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        FanService.objects.create(
            product_name=product_name,
            product_image=product_image,
            service_details=service_details,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect("company:fan_service")

    return render(request, "fan_service.html", {
        "services": services,
        "is_update": False
    })
def update_fan_service(request, id):
    booking = FanService.objects.get(id=id)
    services = FanService.objects.all().order_by("-id")  # ADD THIS LINE

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")
        booking.link = request.POST.get("link")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:fan_service")

    return render(request, "fan_service.html", {
        "booking": booking,
        "services": services,        # PASS SERVICES HERE
        "is_update": True
    })

def delete_fan_service(request, id):
    item = FanService.objects.get(id=id)
    item.delete()
    return redirect("company:fan_service")

#============Geyser Service================#

def geyser_service(request):
    services =  GeyserService.objects.all().order_by("-id")

    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_image = request.FILES.get("productImage")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        GeyserService.objects.create(
            user=request.user,  
            product_name=product_name,
            product_image=product_image,
            service_details=service_details,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect("company:geyser_service")

    return render(request, "geyser_service.html", {
        "services": services,
        "is_update": False
    })
def update_geyser_service(request, id):
    booking = GeyserService.objects.get(id=id)
    services = GeyserService.objects.all().order_by("-id")  # ADD THIS LINE

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")
        booking.link = request.POST.get("link")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:geyser_service")

    return render(request, "geyser_service.html", {
        "booking": booking,
        "services": services,        # PASS SERVICES HERE
        "is_update": True
    })

def delete_geyser_service(request, id):
    item = GeyserService.objects.get(id=id)
    item.delete()
    return redirect("company:geyser_service")
#================Washing Machine==============#
def washing_service(request):
    services =  WashingService.objects.all().order_by("-id")

    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_image = request.FILES.get("productImage")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        WashingService.objects.create(
            user=request.user,  
            product_name=product_name,
            product_image=product_image,
            service_details=service_details,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect("company:washing_service")

    return render(request, "washing_service.html", {
        "services": services,
        "is_update": False
    })
def update_washing_service(request, id):
    booking = WashingService.objects.get(id=id)
    services = WashingService.objects.all().order_by("-id")  # ADD THIS LINE

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")
        booking.link = request.POST.get("link")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:washing_service")

    return render(request, "washing_service.html", {
        "booking": booking,
        "services": services,        # PASS SERVICES HERE
        "is_update": True
    })

def delete_washing_service(request, id):
    item = WashingService.objects.get(id=id)
    item.delete()
    return redirect("company:washing_service")

#================Fridge Service================#
def fridge_service(request):
    services =  FridgeService.objects.all().order_by("-id")

    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_image = request.FILES.get("productImage")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        FridgeService.objects.create(
            user=request.user,  
            product_name=product_name,
            product_image=product_image,
            service_details=service_details,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect("company:fridge_service")

    return render(request, "fridge_service.html", {
        "services": services,
        "is_update": False
    })
def update_fridge_service(request, id):
    booking = FridgeService.objects.get(id=id)
    services = FridgeService.objects.all().order_by("-id")  # ADD THIS LINE

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")
        booking.link = request.POST.get("link")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:fridge_service")

    return render(request, "fridge_service.html", {
        "booking": booking,
        "services": services,        # PASS SERVICES HERE
        "is_update": True
    })

def delete_fridge_service(request, id):
    item = FridgeService.objects.get(id=id)
    item.delete()
    return redirect("company:fridge_service")

#================Water Purifier Service================#
def waterpurifier_service(request):
    services = WaterpurifierService.objects.all().order_by("-id")

    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_image = request.FILES.get("productImage")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        WaterpurifierService.objects.create(
            user=request.user,  
            product_name=product_name,
            product_image=product_image,
            service_details=service_details,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect("company:waterpurifier_service")

    return render(request, "waterpurifier_service.html", {
        "services": services,
        "is_update": False
    })
def update_waterpurifier_service(request, id):
    booking = WaterpurifierService.objects.get(id=id)
    services =WaterpurifierService.objects.all().order_by("-id")  # ADD THIS LINE

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")
        booking.link = request.POST.get("link")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:waterpurifier_service")

    return render(request, "waterpurifier_service.html", {
        "booking": booking,
        "services": services,        # PASS SERVICES HERE
        "is_update": True
    })

def delete_waterpurifier_service(request, id):
    item = WaterpurifierService.objects.get(id=id)
    item.delete()
    return redirect("company:waterpurifier_service")


#================Water Cooler Service================#
def watercooler_service(request):
    services = WatercoolerService.objects.all().order_by("-id")

    if request.method == "POST":
        product_name = request.POST.get("productName")
        product_image = request.FILES.get("productImage")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        WatercoolerService.objects.create(
            user=request.user,  
            product_name=product_name,
            product_image=product_image,
            service_details=service_details,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect("company:watercooler_service")

    return render(request, "watercooler_service.html", {
        "services": services,
        "is_update": False
    })
def update_watercooler_service(request, id):
    booking = WatercoolerService.objects.get(id=id)
    services =WatercoolerService.objects.all().order_by("-id")  # ADD THIS LINE

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")
        booking.link = request.POST.get("link")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:watercooler_service")

    return render(request, "watercooler_service.html", {
        "booking": booking,
        "services": services,        # PASS SERVICES HERE
        "is_update": True
    })

def delete_watercooler_service(request, id):
    item = WatercoolerService.objects.get(id=id)
    item.delete()
    return redirect("company:watercooler_service")




@login_required(login_url='users:admin_login')
def press_service(request):
    services = PressService.objects.all().order_by('-id')

    if request.method == "POST":
        productName = request.POST.get("productName")
        productImage = request.FILES.get("productImage")
        serviceDetails = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        PressService.objects.create(
            product_name=productName,
            product_image=productImage,
            service_details=serviceDetails,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect('company:press_service')

    return render(request, "press_service.html", {
        "services": services,
        "is_update": False
    })
@login_required
def update_press_service(request, id):
    booking = PressService.objects.get(id=id)

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.link = request.POST.get("link")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:press_services")

    return render(request, "company/press_services.html", {
        "booking": booking,
        "is_update": True,
        "services": PressService.objects.all()
    })
@login_required
def delete_press_service(request, id):
    item = PressService.objects.get(id=id)
    item.delete()
    return redirect("company:press_services")

@login_required(login_url='users:admin_login')
def oven_service(request):
    services = OvenService.objects.all().order_by('-id')

    if request.method == "POST":
        productName = request.POST.get("productName")
        productImage = request.FILES.get("productImage")
        serviceDetails = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        OvenService.objects.create(
            product_name=productName,
            product_image=productImage,
            service_details=serviceDetails,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect('company:oven_service')

    return render(request, "oven_service.html", {
        "services": services,
        "is_update": False
    })
@login_required
def update_oven_service(request, id):
    booking = OvenService.objects.get(id=id)

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.link = request.POST.get("link")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:oven_service")

    return render(request, "oven_service.html", {
        "booking": booking,
        "is_update": True,
        "services": PressService.objects.all()
    })
@login_required
def delete_oven_service(request, id):
    item = PressService.objects.get(id=id)
    item.delete()
    return redirect("company:oven_service")





#================Tv Service =================#

def tv_service(request):
    services = TvService.objects.all().order_by('-id')

    if request.method == "POST":
        productName = request.POST.get("productName")
        productImage = request.FILES.get("productImage")
        serviceDetails = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")

        TvService.objects.create(
            product_name=productName,
            product_image=productImage,
            service_details=serviceDetails,
            rating=rating,
            price=price,
            link=link,
            details=details,
            extra_details=extra_details
        )

        return redirect('company:tv_service')

    return render(request, "tv_service.html", {
        "services": services,
        "is_update": False
    })
@login_required
def update_tv_service(request, id):
    booking = TvService.objects.get(id=id)

    if request.method == "POST":
        booking.product_name = request.POST.get("productName")
        booking.service_details = request.POST.get("serviceDetails")
        booking.rating = request.POST.get("rating")
        booking.price = request.POST.get("price")
        booking.link = request.POST.get("link")
        booking.details = request.POST.get("details")
        booking.extra_details = request.POST.get("extra_details")

        if request.FILES.get("productImage"):
            booking.product_image = request.FILES.get("productImage")

        booking.save()
        return redirect("company:tv_service")

    return render(request, "tv_service.html", {
        "booking": booking,
        "is_update": True,
        "services": TvService.objects.all()
    })
@login_required
def delete_tv_service(request, id):
    item = TvService.objects.get(id=id)
    item.delete()
    return redirect("company:tv_service")



#================Laptop Service Views =====================#
def laptop_service(request, id=None):

    booking = None
    is_update = False

    if id:
        booking = get_object_or_404(LaptopService, id=id, user=request.user)
        is_update = True

    if request.method == "POST":

        product_name = request.POST.get("productName")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")
        product_image = request.FILES.get("productImage")

        if is_update:
            booking.product_name = product_name
            booking.service_details = service_details
            booking.rating = rating
            booking.price = price
            booking.link = link
            booking.details = details
            booking.extra_details = extra_details

            if product_image:
                booking.product_image = product_image

            booking.save()
            messages.success(request, "Laptop service updated successfully")

        else:
            LaptopService.objects.create(
                user=request.user,
                product_name=product_name,
                product_image=product_image,
                service_details=service_details,
                rating=rating,
                price=price,
                link=link,
                details=details,
                extra_details=extra_details
            )
            messages.success(request, "Laptop service added successfully")

        return redirect("company:laptop_service")

    services = LaptopService.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "laptop_service.html", {
        "services": services,
        "is_update": is_update,
        "booking": booking
    })


@login_required
def delete_laptop_service(request, id):
    booking = get_object_or_404(LaptopService, id=id, user=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Laptop service deleted successfully")

    return redirect("company:laptop_service")






#==========Inverter Service===========
@login_required
def inverter_service(request, id=None):

    booking = None
    is_update = False

    if id:
        booking = get_object_or_404(InverterService, id=id, user=request.user)
        is_update = True

    if request.method == "POST":

        product_name = request.POST.get("productName")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")
        product_image = request.FILES.get("productImage")

        if is_update:
            booking.product_name = product_name
            booking.service_details = service_details
            booking.rating = rating
            booking.price = price
            booking.link = link
            booking.details = details
            booking.extra_details = extra_details

            if product_image:
                booking.product_image = product_image

            booking.save()
            messages.success(request, "Inverter service updated successfully")

        else:
            InverterService.objects.create(
                user=request.user,
                product_name=product_name,
                product_image=product_image,
                service_details=service_details,
                rating=rating,
                price=price,
                link=link,
                details=details,
                extra_details=extra_details
            )
            messages.success(request, "Inverter service added successfully")

        return redirect("company:inverter_service")

    services = InverterService.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "inverter_service.html", {
        "services": services,
        "is_update": is_update,
        "booking": booking
    })


@login_required
def delete_inverter_service(request, id):
    booking = get_object_or_404(InverterService, id=id, user=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Inverter service deleted successfully")

    return redirect("company:inverter_service")



#---------Chimney Service----------
@login_required
def chimney_service(request, id=None):

    booking = None
    is_update = False

    if id:
        booking = get_object_or_404(ChimneyService, id=id, user=request.user)
        is_update = True

    if request.method == "POST":
        product_name = request.POST.get("productName")
        service_details = request.POST.get("serviceDetails")
        rating = request.POST.get("rating")
        price = request.POST.get("price")
        link = request.POST.get("link")
        details = request.POST.get("details")
        extra_details = request.POST.get("extra_details")
        product_image = request.FILES.get("productImage")

        if is_update:
            booking.product_name = product_name
            booking.service_details = service_details
            booking.rating = rating
            booking.price = price
            booking.link = link
            booking.details = details
            booking.extra_details = extra_details

            if product_image:
                booking.product_image = product_image

            booking.save()
            messages.success(request, "Chimney service updated successfully")

        else:
            ChimneyService.objects.create(
                user=request.user,
                product_name=product_name,
                product_image=product_image,
                service_details=service_details,
                rating=rating,
                price=price,
                link=link,
                details=details,
                extra_details=extra_details
            )
            messages.success(request, "Chimney service added successfully")

        return redirect("company:chimney_service")

    services = ChimneyService.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "chimney_service.html", {
        "services": services,
        "is_update": is_update,
        "booking": booking
    })


@login_required
def delete_chimney_service(request, id):
    booking = get_object_or_404(ChimneyService, id=id, user=request.user)
    booking.delete()
    messages.success(request, "Chimney service deleted successfully")
    return redirect("company:chimney_service")

#================feadback and review ===================#
@login_required(login_url='users:admin_login')
def review(request):
    # Optional: restrict to admin/staff only
    if not request.user.is_staff:
        return redirect("users:index")

    reviews = OrderFeedback.objects.select_related("user").order_by("-created_at")

    return render(request, "review.html", {
        "reviews": reviews
    })

@login_required
def delete_feedback(request, feedback_id):
    # 🔒 Only admin/staff can delete
    if not request.user.is_staff:
        messages.error(request, "Unauthorized access.")
        return redirect("users:index")

    feedback = get_object_or_404(OrderFeedback, id=feedback_id)
    feedback.delete()

    messages.success(request, "Feedback deleted successfully.")
    return redirect("company:review")

@staff_member_required
def cancelorder(request):

    cancelled_orders = (
        CancelDetails.objects
        .select_related('user')
        .order_by('-cancelled_at')
    )

    # Orders + items
    orders = (
        MyOrder.objects
        .filter(id__in=[c.order_id for c in cancelled_orders])
        .prefetch_related("items")
    )

    # order_id → order object
    order_map = {o.id: o for o in orders}

    # =========================
    # 🏢 SERVICE CENTER (PINCODE WISE)
    # =========================
    pincodes = orders.values_list("pincode", flat=True).distinct()

    servicecenters = ServiceCenterRegister.objects.filter(
        pincode__in=pincodes
    )

    servicecenter_map = {
        sc.pincode: sc for sc in servicecenters
    }

    return render(request, 'cancelorder.html', {
        'cancelled_orders': cancelled_orders,
        'orders': order_map,
        'servicecenter_map': servicecenter_map,
    })


#===============Order=================#

@staff_member_required
def company_orders(request):
    orders = MyOrder.objects.all().order_by("-created_at")

    # =========================
    # 🧾 Complaints
    # =========================
    complaints = OrderComplaint.objects.select_related("order", "user")

    complaint_map = {}
    for c in complaints:
        complaint_map.setdefault(c.order_id, []).append(c)

    # =========================
    # 🏢 SERVICE CENTER (PINCODE WISE)
    # =========================
    pincodes = orders.values_list("pincode", flat=True).distinct()

    servicecenters = ServiceCenterRegister.objects.filter(
        pincode__in=pincodes
    )

    # Map → pincode : servicecenter
    servicecenter_map = {
        sc.pincode: sc for sc in servicecenters
    }

    context = {
        "orders": orders,
        "complaint_map": complaint_map,
        "servicecenter_map": servicecenter_map,
    }

    return render(request, "company_orders.html", context)

def delete_company_order(request, order_id):
    order = get_object_or_404(MyOrder, id=order_id)
    order.delete()
    messages.success(request, "Order deleted successfully")
    return redirect("company:company_orders")


#==================See all=====================#

def see_all_product(request):
    if request.method == "POST":
        product_name = request.POST.get('productName')

        if not product_name:
            return redirect('company:see_all_product')

        Product.objects.create(
            productName=product_name,
            productImage=request.FILES.get('productImage'),
            serviceDetails=request.POST.get('serviceDetails'),
            rating=request.POST.get('rating'),
            price=request.POST.get('price'),
            link=request.POST.get('link'),
            details=request.POST.get('details'),
            extra_details=request.POST.get('extra_details'),
        )

        return redirect('company:see_all_product')

    products = Product.objects.all().order_by('-created_at')
    return render(request, 'see_all_product.html', {'products': products})


def update_see_all_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.productName = request.POST.get("productName")  # ✅ FIXED
        product.serviceDetails = request.POST.get("serviceDetails")
        product.rating = request.POST.get("rating")
        product.price = request.POST.get("price")
        product.link = request.POST.get("link")
        product.details = request.POST.get("details")
        product.extra_details = request.POST.get("extra_details")

        if request.FILES.get("productImage"):
            product.productImage = request.FILES.get("productImage")

        product.save()
        return redirect("company:see_all_product")

    return render(
        request,
        "see_all_product.html",
        {
            "products": Product.objects.all().order_by("-created_at"),
            "booking": product,
            "is_update": True
        }
    )



def delete_see_all_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.delete()
        return redirect("company:see_all_product")
    return render(request, "see_all_product.html", {"product":product})



def userprofile(request):
    profile = UserProfile.objects.all().order_by("-created_at")

    return render(request, 'userprofile.html', {
        'profile': profile
    })



def add_slider(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        link_name = request.POST.get('link_name')

        if image:
            Slider.objects.create(
                image=image,
                link_name=link_name
            )
            return redirect('company:add_slider')

    sliders = Slider.objects.all().order_by('-id')

    return render(request, 'add_slider.html', {
        'sliders': sliders
    })


def delete_slider(request, id):
    slider = get_object_or_404(Slider, id=id)

    if request.method == "POST":
        slider.image.delete(save=False)  # delete file from media
        slider.delete()                  # delete record

    return redirect('company:add_slider')


def add_advertisement(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        if image:
            Advertisement.objects.create(image=image)
            return redirect('company:add_advertisement')  # refresh page after save

    # fetch all advertisements
    ads = Advertisement.objects.all().order_by('-created_at')

    return render(request, 'add_advertisement.html', {
        'ads': ads
    })

def update_advertisement(request, ad_id):
    ad = get_object_or_404(Advertisement, id=ad_id)

    if request.method == "POST":
        image = request.FILES.get('image')

        if image:
            ad.image = image
            ad.save()
            return redirect('company:add_advertisement')

    return render(request, 'add_advertisement.html', {
        'ad': ad
    })

def add_advertisement_1(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        if image:
            Advertisement1.objects.create(image=image)
            return redirect('company:add_advertisement_1')

    # fetch saved ads
    ads1 = Advertisement1.objects.all().order_by('-created_at')

    return render(request, "add_advertisement_1.html", {
        "ads1": ads1
    })

#===================Service Center ========================#

def register_servicecenter(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        servicecenter_name = request.POST.get('servicecenter_name')
        author_name = request.POST.get('author_name')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        aadhaar = request.POST.get('aadhaar')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username:
            messages.error(request, "Username is required")
            return redirect('company:register_servicecenter')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('company:register_servicecenter')

        if ServiceCenterRegister.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('company:register_servicecenter')

        ServiceCenterRegister.objects.create(
            username=username,
            servicecenter_name=servicecenter_name,
            author_name=author_name,
            district=district,
            state=state,
            pincode=pincode,
            aadhaar=aadhaar,
            mobile=mobile,
            email=email,
            password=make_password(password)
        )

        messages.success(request, 'Service Center Registered Successfully')
        return redirect('company:register_servicecenter')

    return render(request, 'register_servicecenter.html')






#=============Logout=================#
def logout_admin(request):
    auth_logout(request)
    return redirect("users:admin_login") 

def servicecenter_list(request):
    servicecenters = ServiceCenterRegister.objects.all().order_by('-created_at')
    return render(request, 'servicecenter_list.html', {
        'servicecenters': servicecenters
    })



def update_servicecenter(request, id):
    servicecenter = get_object_or_404(ServiceCenterRegister, id=id)

    if request.method == 'POST':
        servicecenter.servicecenter_name = request.POST.get('servicecenter_name')
        servicecenter.author_name = request.POST.get('author_name')
        servicecenter.district = request.POST.get('district')
        servicecenter.state = request.POST.get('state')
        servicecenter.pincode = request.POST.get('pincode')
        servicecenter.mobile = request.POST.get('mobile')
        servicecenter.email = request.POST.get('email')
        servicecenter.save()

        return redirect('company:servicecenter_list')

    return render(request, 'update_servicecenter.html', {
        'servicecenter': servicecenter
    })

def delete_servicecenter(request, id):
    servicecenter = get_object_or_404(ServiceCenterRegister, id=id)
    servicecenter.delete()
    return redirect('company:servicecenter_list')

def manage_policy(request):
    policy, created = Policy.objects.get_or_create(
        id=1,
        defaults={
            "title": "Privacy & Service Policy",
            "content": ""
        }
    )

    if request.method == "POST":
        policy.title = request.POST.get("title")
        policy.content = request.POST.get("content")
        policy.save()

        messages.success(request, "Policy updated successfully!")

        return redirect("company:manage_policy")

    return render(request, "manage_policy.html", {
        "policy": policy
    })

class CompanyDashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "status": True,
            "data": {
                "total_orders": MyOrder.objects.count(),
                "total_cancel_orders": CancelDetails.objects.count(),
                "total_customers": UserProfile.objects.count()
            }
        })