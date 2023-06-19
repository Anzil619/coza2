
# Register your models here.

from django.contrib import admin
from .models import Order, OrderItem, ReturnOrder, UserCoupon, Coupon

# Register your models here.


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(UserCoupon)
admin.site.register(ReturnOrder)

