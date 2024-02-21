from django.db import models
from django.contrib.auth.models import User as MainUser
import datetime
import secrets
from .paystack import *
from django.db.models.signals import post_save


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=150)
    address = models.CharField(max_length=500, null=True, blank=True) 
    gps_location = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.FloatField(max_length=500, null=True, blank=True)
    longitude = models.FloatField(max_length=500, null=True, blank=True)
    plan = models.OneToOneField("Repair_App.Plan", on_delete=models.DO_NOTHING, null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class Repair_Details(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    gadget_model = models.CharField(max_length=500)
    gadget_IMEI = models.CharField(max_length=500)
    purchase_date = models.DateTimeField()
    complaint_description = models.TextField()
    gadget_image1 = models.ImageField(upload_to="static/Gadget Repair Image", max_length=None, null=False, blank=False)
    gadget_image2 = models.ImageField(upload_to=f"static/Gadget Repair Image", max_length=None, null=True, blank=True)
    gadget_image3 = models.ImageField(upload_to="static/Gadget Repair Image", max_length=None, null=True, blank=True)
    datetime_of_complaint = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Repair details by {self.customer.user.username} @ {self.datetime_of_complaint} " 


class Payment(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, null=True, blank=True)
    amount = models.PositiveIntegerField()
    repair_detail = models.ForeignKey(Repair_Details, on_delete=models.DO_NOTHING, null=True, blank=True)
    ref = models.CharField(max_length=150)
    payment_reason = models.TextField(null=True, blank=True)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey("Repair_App.Plan", on_delete=models.DO_NOTHING, null=True, blank=True)
    consultation_id = models.ForeignKey("Repair_App.Consultation", on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        ordering = ('payment_date',)

    def __str__(self) -> str:
        return f'Payment made at {self.payment_date} by {self.user}'
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(60)
            available_ref = Payment.objects.filter(ref=ref)
            if not available_ref:
                self.ref = ref
                # self.amount = 75000

        super().save(*args, **kwargs)

    def amount_paid(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)

        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save

        if self.verified:
            return True
        
        else:
            return False
       
                
class Contact(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    subject = models.CharField(max_length=5000)
    message = models.TextField()


class Complain(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    subject = models.CharField(max_length=5000)
    complains = models.TextField()


class Plan(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=500, blank=True, null=True)
    benefits1 = models.CharField(max_length=500, blank=True, null=True)
    benefits2 = models.CharField(max_length=500, blank=True, null=True)
    benefits3 = models.CharField(max_length=500, blank=True, null=True)
    benefits4 = models.CharField(max_length=500, blank=True, null=True)
    benefits5 = models.CharField(max_length=500, blank=True, null=True)
    rules = models.TextField()
    
    
    def __str__(self):
        return self.name


class Swap_Deal(models.Model):
    user = models.ForeignKey(Customer, related_name="Initiator", verbose_name=("Initiator"), on_delete=models.DO_NOTHING)
    item_name = models.CharField(max_length=500, blank=True, null=True)                              
    item_description = models.CharField(max_length=500, blank=True, null=True)
    item_pic1 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
    item_pic2 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
    item_pic3 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
    item_pic4 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
    item_pic5 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
    item_needed = models.CharField(max_length=500, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Swap deal by {self.user.user.username} at {self.date_created}"



# class Swap_Deal(models.Model):
#     user1 = models.ForeignKey(Customer, related_name="Initiator", verbose_name=("Initiator"), on_delete=models.DO_NOTHING)
#     user2 = models.ForeignKey(Customer, related_name="Receptor",  verbose_name=("Receptor"), on_delete=models.DO_NOTHING)
#     item_name = models.CharField(max_length=500, blank=True, null=True)                              
#     item_description = models.CharField(max_length=500, blank=True, null=True)
#     item_pic1 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
#     item_pic2 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
#     item_pic3 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
#     item_pic4 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
#     item_pic5 = models.ImageField(upload_to="static/Swap_Deal_Images",max_length=None, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_modified = models.DateTimeField(auto_now=True)
#     date_modified = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Swap deal by {self.name} at {self.date_created}"



class Service_Card(models.Model):
    height = models.IntegerField(default=711)
    width = models.IntegerField(default=800)
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='static/images', help_text="Height: 711 & Width: 800", null=True, blank=True)
    button_text = models.CharField(max_length=50, null=True, blank=True)
    button_redirect_url = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Consultation(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    customer = models.ForeignKey("Repair_App.Customer", on_delete=models.DO_NOTHING, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    subject = models.CharField(max_length=5000)
    complains = models.TextField()
    ref = models.CharField(max_length=150, null=True, blank=True)
