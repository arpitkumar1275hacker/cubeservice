from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class HomeService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    productName = models.CharField(max_length=200)
    productImage = models.ImageField(upload_to="home_services/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName
class PopularBooking(models.Model):
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='popular_images/')  # Image saved in MEDIA_ROOT/popular_images/
    service_details = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=50)  # Only one word as you mentioned
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    

class ProductBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    productName = models.CharField(max_length=200)
    productImage = models.ImageField(upload_to="popular_booking/")
    serviceDetails = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=50)  # Only one word as you mentioned
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName
    
    
class SessionalBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    productName = models.CharField(max_length=200)
    productImage = models.ImageField(upload_to="popular_booking/")
    serviceDetails = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=50)  # Only one word as you mentioned
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName
#=============Ac Service Model ==============#    
class ACService(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="ac_service/")
    service_details = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=100)
    details = models.TextField()
    extra_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


#=============Fan Service Model=============#

class FanService(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="fan_services/")
    service_details = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    link = models.CharField(max_length=200)
    details = models.TextField()
    extra_details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
    #=============Press Service Model =================#
class PressService(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="press_services/")
    service_details = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=200)
    details = models.TextField()
    extra_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    

        #=============Oven Service Model =================#
class OvenService(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="oven_services/")
    service_details = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=200)
    details = models.TextField()
    extra_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    

    
        #=============Tv Service Model =================#
class TvService(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="oven_services/")
    service_details = models.TextField()
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.CharField(max_length=200)
    details = models.TextField()
    extra_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    

    #########Laptop Service##########>
class LaptopService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="laptop_services/")
    service_details = models.TextField()

    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)

    details = models.TextField()
    extra_details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
#==================Geyser Service=================#
class GeyserService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="laptop_services/")
    service_details = models.TextField()

    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)

    details = models.TextField()
    extra_details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    

    #===========Washing Service =============#
class WashingService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="laptop_services/")
    service_details = models.TextField()

    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)

    details = models.TextField()
    extra_details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    

    
    #===========Water Purifier Service =============#
class WaterpurifierService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="laptop_services/")
    service_details = models.TextField()

    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)

    details = models.TextField()
    extra_details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


#==================Water Cooler Service=================#
class WatercoolerService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="laptop_services/")
    service_details = models.TextField()

    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)

    details = models.TextField()
    extra_details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    
class FridgeService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="laptop_services/")
    service_details = models.TextField()

    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)

    details = models.TextField()
    extra_details = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


    #-------------Inverter Service-----------
class InverterService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="inverter_services/")
    service_details = models.CharField(max_length=300)
    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)
    details = models.TextField()
    extra_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name




#--------Chimney------
class ChimneyService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="chimney/")
    service_details = models.CharField(max_length=300)
    rating = models.IntegerField(default=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField(max_length=500)
    details = models.TextField()
    extra_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


        

class Product(models.Model):
    productName = models.CharField(max_length=200)
    productImage = models.ImageField(upload_to='products/', null=True, blank=True)
    serviceDetails = models.TextField(null=True)
    rating = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=255)

    details = models.TextField()          # ✅ THIS
    extra_details = models.TextField()    # ✅ THIS

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.productName


class Slider(models.Model):
    image = models.ImageField(upload_to='sliders/')
    created_at = models.DateTimeField(auto_now_add=True)
    link_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Slider {self.id}"

      





class Advertisement(models.Model):
    image = models.ImageField(upload_to='ads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ad {self.id}"

class Advertisement1(models.Model):
    image = models.ImageField(upload_to="advertisement_1/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Advertisement1 {self.id}"



class ServiceCenterRegister(models.Model):
    username = models.CharField(max_length=50, unique=True)
    servicecenter_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    aadhaar = models.CharField(max_length=12, unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
       return self.username

class Policy(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title