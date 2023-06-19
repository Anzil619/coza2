from django.db import models
from accounts.models import CustomUser
from store.models import Product

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.product) + ' by ' + str(self.user.username)

