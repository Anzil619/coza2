from django.db import models
from accounts.models import CustomUser

from store.models import Product, Variation

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        if self.product.offer:
            return self.product.get_offer_price() * self.quantity
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product
    
   

