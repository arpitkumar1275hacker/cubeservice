from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fullname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField()

    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
   

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mobile
    
class Admin(models.Model):
   username = models.CharField(max_length=150, unique=True)
   email = models.EmailField(unique=True)
  
def __str__(self):
        return self.username

class Add_Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service_name = models.CharField(max_length=255)
    service_details = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    extra_details = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)  #


class MyOrder(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    fullname = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)
    email = models.CharField(max_length=55)
    date = models.CharField(max_length=55)
    address = models.TextField()
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    total_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔹 NEW FIELDS (FOR SERVICE CENTER)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    service_center = models.ForeignKey(
        "company.ServiceCenterRegister",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.fullname} ({self.status})"





class OrderItem(models.Model):
    order = models.ForeignKey(
        MyOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    service_name = models.TextField()
    service_details = models.TextField()
    details = models.TextField()
    extra_details = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.URLField()

    def __str__(self):
        return self.service_name

    
class CancelDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.IntegerField()   # 👈 Order model से relation नहीं
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Requested', 'Requested'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
        ],
        default='Requested'
    )
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancel Order ID {self.order_id}"
    

    
# models.py
# models.py
class OrderFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(MyOrder, on_delete=models.CASCADE)  # ❗ REQUIRED
    service_name = models.CharField(max_length=255)   # 👈 IMPORTANT
    rating = models.IntegerField()
    message = models.TextField()
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name} - {self.rating}⭐"


class OrderComplaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('MyOrder', on_delete=models.CASCADE)
    service_name = models.TextField()
    complaint_text = models.TextField()

    complaint_audio = models.FileField(
        upload_to='complaints/audio/',
        blank=True,
        null=True
    )

    complaint_image = models.ImageField(   # ✅ NEW
        upload_to='complaints/images/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint - Order {self.order.id}"

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    pincode = models.CharField(max_length=6)   # ✅ ADD THIS
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.mobile}"