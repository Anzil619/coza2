from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from carts.views import _cart_id
from accounts.models import CustomUser
from userprofile.models import Address
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from store.models import Product
from . models import Coupon, Order, OrderItem, ReturnOrder, UserCoupon
from django.shortcuts import render, redirect
import csv
import random


# Create your views here.

@cache_control(no_cache=True,must_revalidate=True,no_store=True)    
@login_required(login_url='user_login')
def checkout(request,total=0, quantity=0, cart_item=None):  
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:        
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer:
                total += (cart_item.product.get_offer_price() * cart_item.quantity)
            else:
                total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    address = Address.objects.filter(user = request.user)
    coupons = Coupon.objects.filter(active = True)
    print(coupons,"daxii")
    context = {
        'cart_items' : cart_items,
        'quantity' : quantity,
        'total' : total,
        'tax' : tax,
        'grand_total' : grand_total,
        'address' : address,
        'coupons': coupons,
        'usercoupon': UserCoupon.objects.filter(user=request.user),
    }
    return render(request,'store/checkout.html',context)



@login_required(login_url='user_login')
def placeorder(request):
   
    if request.method == 'POST':

        # coupon_code = request.POST['coupon']
        
        neworder = Order()
        neworder.user = request.user
        address_id = request.POST['address']
    
        address = Address.objects.get(id=address_id)
        neworder.address = address
        payment_mode = request.POST.get('payment_method')
        neworder.payment_mode = payment_mode

        neworder.payment_id = request.POST.get('payment_id')

        cart = CartItem.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            if item.product.offer:

                cart_total_price = item.product.get_offer_price() * item.quantity

            else:
                cart_total_price += item.product.price * item.quantity
            # item.product.stock-=item.quantity
        tax = (2*cart_total_price)/100
        neworder.total_price = cart_total_price + tax
        trackno = random.randint(1111111, 9999999)

        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno
        neworder.save()


        try:
            instance = UserCoupon.objects.get(user=request.user)

            if float(cart_total_price) >= float(instance.coupon.min_value):
                coupon_discount = (
                    (float(cart_total_price) * float(instance.coupon.discount))/100)
                cart_total_price = float(cart_total_price) - coupon_discount
                cart_total_price = format(cart_total_price, '.2f')
                coupon_discount = format(coupon_discount, '.2f')

            instance.delete()
            neworder.total_price = cart_total_price
            neworder.save()

        except:
            pass


        neworderitems = CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
                
            )

            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            orderproduct.save()

        

            
        if (payment_mode== 'wallet_payment'):
            
            wallet = CustomUser.objects.get(email=request.user)
            if float(cart_total_price) >= float(wallet.wallet):
               messages.error(request, 'Wallet does not have the required amount')
               return redirect(checkout)
            
            wallet.wallet -= cart_total_price
            wallet.save()
                

        # To clear user Cart
        CartItem.objects.filter(user=request.user).delete()
        

        context={
            'order' : OrderItem.objects.filter(order=neworder),
        }

    return render(request, 'order/order_success.html', context)



def razarypaycheck(request):
    cart = CartItem.objects.filter(user=request.user)
    total_price = 0
    
    for item in cart:
        if item.product.offer:
            total_price += item.product.get_offer_price() * item.quantity
        else:
            total_price = total_price + item.product.price * item.quantity
    try:
        instance = UserCoupon.objects.get(user=request.user)
        total_price = instance.total_price
    except:
        pass
    tax = (2*total_price)/100
    total_price = round(total_price+tax)

    return JsonResponse({'total_price': total_price})




def sample(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        address_id = request.POST['address']
        address = Address.objects.get(id=address_id)
        neworder.address = address
        neworder.payment_mode = request.POST.get('payment_method')
        neworder.payment_id = request.POST.get('payment_id')

        cart = CartItem.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            if item.product.offer:
                cart_total_price += item.product.get_offer_price() * item.quantity
            else:
                cart_total_price += item.product.price * item.quantity
        
        try:
            instance = UserCoupon.objects.get(user=request.user)

            if float(cart_total_price) >= float(instance.coupon.min_value):
                coupon_discount = (
                    (float(cart_total_price) * float(instance.coupon.discount))/100)
                cart_total_price = float(cart_total_price) - coupon_discount
                cart_total_price = format(cart_total_price, '.2f')
                coupon_discount = format(coupon_discount, '.2f')

            instance.delete()
            neworder.total_price = cart_total_price
            neworder.save()

        except:
            pass

        tax = round((2*cart_total_price)/100)
        neworder.total_price = cart_total_price + tax
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = CartItem.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,      
            )
            # To decrease the product quantity from available stock
        orderproduct = Product.objects.filter(id=item.product.id).first()
        orderproduct.stock = orderproduct.stock - item.quantity
        orderproduct.save()
        payment_mode = request.POST.get('payment_method')
        if (payment_mode== 'Razorpay'):
            CartItem.objects.filter(user=request.user).delete()
            return JsonResponse({'status' : "Your order has been succesfully placed"})

        # To clear user Cart
        CartItem.objects.filter(user=request.user).delete()
    return redirect('checkout')


def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-update_at')
    orderitems = OrderItem.objects.filter(order__in=orders).order_by('-order__update_at')
    context = {
        'orders': orders,
        'orderitems': orderitems,
    }
    return render(request, 'order/order_list.html', context)




def ordercancel(request):
    
    order_id = request.POST.get('order_id')
    order_item_id= request.POST.get('orderitem_id')
    orders = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.get(id=order_item_id)

    if orders.payment_mode == 'Razorpay' or 'wallet_payment':
        wallet = CustomUser.objects.get(email=request.user)
        wallet.wallet += orders.total_price
        wallet.save()

    order_items.product.stock+=order_items.quantity
    order_items.status = 'Cancelled'
    order_items.save()
    return redirect('orders')


    
def order_return(request,id):
    order_item = OrderItem.objects.get(id=id)
    wallet = 0
    if request.method == "POST":
        return_reason = request.POST.get('return_reason')
        return_comment = request.POST.get('return_comment')
        ReturnOrder.objects.create(order_item=order_item,return_reason= return_reason, return_comment=return_comment)
        order_item.status = "Returned"
        order_item.product.stock+= order_item.quantity
        order_item.save()

        wallet=CustomUser.objects.get(email=request.user)
        wallet.wallet += order_item.order.total_price
        wallet.save()
        print(wallet.wallet,"daxo")

    return redirect('orders')

    



def coupons(request):
    if request.method == 'POST':
        coupon_code = request.POST['coupon']
        
        
        grand_total = request.POST['grand_total']
        if UserCoupon.objects.filter(user=request.user).exists():
            
            UserCoupon.objects.filter(user=request.user).delete()

        coupon_discount = 0
        if Coupon.objects.get(code=coupon_code):
            instance = Coupon.objects.get(code=coupon_code)
            print("shumban")
            if float(grand_total) >= float(instance.min_value):
                coupon_discount = (
                    (float(grand_total) * float(instance.discount))/100)
                
                grand_total = float(grand_total) - coupon_discount
                grand_total = format(grand_total, '.2f')
                coupon_discount = format(coupon_discount, '.2f')
                msg = 'Coupon Applied successfully'
                UserCoupon.objects.create(user=request.user, coupon = instance, used = True, total_price = grand_total)
                instance.active = False
                instance.save()
                print(grand_total,'daxo')
            else:
                msg = 'This coupon is only applicable for orders more than ₹' + \
                    str(instance.min_value) + '\- only!'
        
            msg = 'Coupon is not valid'

        response = {
            
            'grand_total': grand_total,
            'msg': msg,
            'coupon_discount': coupon_discount,
            'coupon_code': coupon_code,
        }

    return JsonResponse(response)


def single_order_details(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return redirect('orders')
    address_id=order.address.id
    address = Address.objects.get(id=address_id)
    print(address,"aami")
    order_items = OrderItem.objects.filter(order_id=id)
    print(order_items,"aami")

    context ={
        'order_item' : order_items,
        'address'    : address,
        'order'   : order,
    }

    return render (request, 'order/single_order.html', context)




def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no'])

    expenses = Order.objects.all()
    for expense in expenses:
        writer.writerow([expense.user, expense.total_price, expense.payment_mode,expense.tracking_no])

    return response





