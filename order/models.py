from django.db import models
from userprofile.models import Address
from store.models import Product
from accounts.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator
# # Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null= False)
    payment_id = models.CharField(max_length=250, null=True)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.tracking_no)
    

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    status = models.CharField(max_length=150,choices=STATUS, default='Order Confirmed')

    def _str_(self):
        return f"{self.order.id, self.order.tracking_no}"
    

class ReturnOrder(models.Model):
    order_item = models.ForeignKey(OrderItem,on_delete=models.CASCADE)
    return_reason = models.CharField(max_length=100,null=True)
    return_comment = models.TextField(max_length=500,null=True)
    
    def __str__(self):
        return f"{self.id}"
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])
    min_value = models.IntegerField(validators=[MinValueValidator(0)])
    valid_from = models.DateField(auto_now_add=True)
    valid_till = models.DateField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    

class UserCoupon(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    total_price = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)
    

    


