from django.shortcuts import render
from django.shortcuts import render, redirect
from company.models import ServiceCenterRegister
from users.models import MyOrder, OrderItem
from users.models import CancelDetails
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from users.models import OrderFeedback
from users.models import Contact
from users.models import UserProfile,OrderComplaint
# Create your views here.
def servicecenterdashboard(request):
    servicecenter_id = request.session.get('servicecenter_id')

    if not servicecenter_id:
        return redirect('company:login_servicecenter')

    servicecenter = ServiceCenterRegister.objects.get(id=servicecenter_id)

    context = {
        'servicecenter': servicecenter
    }
    return render(request, 'servicecenterdashboard.html', context)


def servicecenter_profile(request):
    servicecenter_id = request.session.get('servicecenter_id')

    if not servicecenter_id:
        return redirect('company:login_servicecenter')

    servicecenter = ServiceCenterRegister.objects.get(id=servicecenter_id)

    return render(request, 'servicecenter_profile.html', {
        'servicecenter': servicecenter
    })

def edit_servicecenter_profile(request):
    servicecenter_id = request.session.get('servicecenter_id')

    if not servicecenter_id:
        return redirect('company:login_servicecenter')

    servicecenter = ServiceCenterRegister.objects.get(id=servicecenter_id)

    if request.method == 'POST':
        servicecenter.servicecenter_name = request.POST.get('servicecenter_name')
        servicecenter.author_name = request.POST.get('author_name')
        servicecenter.email = request.POST.get('email')
        servicecenter.mobile = request.POST.get('mobile')
        servicecenter.district = request.POST.get('district')
        servicecenter.state = request.POST.get('state')
        servicecenter.pincode = request.POST.get('pincode')

        servicecenter.save()
        return redirect('servicecenter:servicecenter_profile')

    return render(request, 'edit_servicecenter_profile.html', {
        'servicecenter': servicecenter
    })

def servicecenter_orders(request):
    servicecenter_id = request.session.get("servicecenter_id")
    if not servicecenter_id:
        return redirect("users:login_servicecenter")

    district = request.session.get("district")
    pincode = request.session.get("pincode")

    # 🔹 ORDERS
    orders = MyOrder.objects.filter(
        district__iexact=district,
        pincode=pincode
    ).prefetch_related("items").order_by("-created_at")

    # 🔹 ORDER COUNTS
    total_orders = orders.count()
    accepted_orders = orders.filter(status="accepted").count()
    rejected_orders = orders.filter(status="rejected").count()
    pending_orders = orders.filter(status="pending").count()

    # 🔥 COMPLAINTS (PINCODE + DISTRICT WISE)
    complaints = OrderComplaint.objects.filter(
        user__userprofile__district__iexact=district,
        user__userprofile__pincode=pincode
    ).select_related("order", "user").order_by("-created_at")

    return render(request, "servicecenter_orders.html", {
        "orders": orders,
        "complaints": complaints,   # ✅ NEW
        "total_orders": total_orders,
        "accepted_orders": accepted_orders,
        "rejected_orders": rejected_orders,
        "pending_orders": pending_orders,
    })

@require_POST
def accept_order(request, order_id):
    servicecenter_id = request.session.get("servicecenter_id")

    if not servicecenter_id:
        return redirect("company:login_servicecenter")

    order = get_object_or_404(
        MyOrder,
        id=order_id,
        status="pending"
    )

    order.status = "accepted"
    order.service_center_id = servicecenter_id
    order.save()

    messages.success(request, "Order accepted successfully")
    return redirect("servicecenter:servicecenter_orders")

@require_POST
def reject_order(request, order_id):
    servicecenter_id = request.session.get("servicecenter_id")

    if not servicecenter_id:
        return redirect("servicecenter:login_servicecenter")

    order = get_object_or_404(
        MyOrder,
        id=order_id,
        status="pending"
    )

    order.status = "rejected"
    order.save()

    messages.error(request, "Order rejected")
    return redirect("servicecenter:servicecenter_orders")

#===========cancel order==================#
def service_cancel_orders(request):

    servicecenter_id = request.session.get("servicecenter_id")
    if not servicecenter_id:
        return redirect("company:login_servicecenter")

    service_pincode = request.session.get("pincode")

    if not service_pincode:
        return render(request, "service_cancel_orders.html", {
            "cancelled_orders": [],
            "cancel_map": {},
            "error": "Pincode not found"
        })

    # 1️⃣ Get cancelled order IDs
    cancelled_ids = CancelDetails.objects.values_list(
        "order_id", flat=True
    )

    # 2️⃣ Fetch cancelled orders for service area
    cancelled_orders = (
        MyOrder.objects
        .filter(id__in=cancelled_ids, pincode=service_pincode)
        .order_by("-created_at")
    )

    # 3️⃣ Map cancel reasons
    cancel_map = {
        c.order_id: c.reason
        for c in CancelDetails.objects.filter(order_id__in=cancelled_ids)
    }

    return render(request, "service_cancel_orders.html", {
        "cancelled_orders": cancelled_orders,
        "cancel_map": cancel_map
    })


def servicecenter_feedback(request):
    servicecenter_id = request.session.get('servicecenter_id')

    if not servicecenter_id:
        return redirect('company:login_servicecenter')

    servicecenter = ServiceCenterRegister.objects.get(id=servicecenter_id)

    feedbacks = OrderFeedback.objects.filter(
        pincode=servicecenter.pincode
    ).order_by('-created_at')

    context = {
        'feedbacks': feedbacks,
        'servicecenter': servicecenter
    }
    return render(request, 'servicecenter_feedback.html', context)


def servicecenter_logout(request):
    request.session.flush()   # 🔥 clears all session data
    return redirect("users:login_servicecenter")



def customers_list(request):
    # service center pincode (optional restriction)
    service_pincode = request.session.get('pincode')

    # filter input from search box
    search_pincode = request.GET.get('pincode')

    customers = UserProfile.objects.all()

    # If service center should only see their area customers
    if service_pincode:
        customers = customers.filter(pincode=service_pincode)

    # If filter box is used
    if search_pincode:
        customers = customers.filter(pincode=search_pincode)

    context = {
        'customers': customers
    }

    return render(request, 'customers_list.html', context)

def servicecenter_contacts(request):
    if not request.session.get("servicecenter_id"):
        return redirect("company:login_servicecenter")

    servicecenter_pincode = request.session.get("pincode")

    contacts = Contact.objects.filter(
        pincode=servicecenter_pincode
    ).order_by("-created_at")

    # DELETE CONTACT
    if request.method == "POST":
        contact_id = request.POST.get("delete_id")
        Contact.objects.filter(id=contact_id).delete()
        return redirect("servicecenter:servicecenter_contacts")

    return render(request, "servicecenter_contacts.html", {
        "contacts": contacts
    })




