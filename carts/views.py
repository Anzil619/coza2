from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Product, Variation, Cart, CartItem
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    
    if current_user.is_authenticated:
        product_variation = []
        
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass
        
        

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id_list = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)

            match_found = False
            for ex_vars in ex_var_list:
                if set(ex_vars) == set(product_variation):
                    match_found = True
                    break

            if match_found:
                index = ex_var_list.index(ex_vars)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()


                
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        
            
        return redirect('cart')


    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()
            

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id_list = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id_list.append(item.id)

            match_found = False
            for ex_vars in ex_var_list:
                if set(ex_vars) == set(product_variation):
                    match_found = True
                    break

            if match_found:
                index = ex_var_list.index(ex_vars)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
                # return HttpResponse('true')
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
                # return HttpResponse('false')
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        
            
        return redirect('cart')





def remove_cart(request):
    product_id = request.POST.get('product_id')
    cart_item_id = request.POST.get('cart_item_id')
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

            carts = CartItem.objects.filter(user=request.user).order_by('id')
            total_price = 0
            
            for item in carts:
                if item.product.offer:
                    total_price=total_price + item.product.get_offer_price() * item.quantity
                else:
                    total_price=total_price + item.product.price * item.quantity
            if product.offer:
                single_pro_total = product.get_offer_price() * item.quantity
            else:
                single_pro_total = product.price*cart_item.quantity

            return JsonResponse({'status' : 'updated succesfully','sub_total': total_price,'single_pro_total': single_pro_total})
        else:
            cart_item.delete()
    except:
        return JsonResponse({'status' : 'Failed'})


def increment_cart(request):
    product_id = request.POST.get('product_id')
    cart_item_id = request.POST.get('cart_item_id')
    product_qty = int(request.POST.get('qty'))
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.product.stock<product_qty:
            return JsonResponse({'status':"not"})
                
        cart_item.quantity += 1
        cart_item.save()

        carts = CartItem.objects.filter(user=request.user).order_by('id')
        total_price = 0
        for item in carts:
            if item.product.offer:
                total_price += item.product.get_offer_price() * item.quantity     
            else: 
                total_price=total_price+ item.product.price * item.quantity

        if product.offer:
            single_pro_total= product.get_offer_price() * item.quantity
        else:
            single_pro_total = product.price*cart_item.quantity

        return JsonResponse({'sub_total': total_price,'single_pro_total': single_pro_total })
    except:
        return JsonResponse({'sub_total': total_price,'single_pro_total': single_pro_total})




def cart(request ,total=0, quantity=0, cart_item=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            print(cart_items,"da")
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

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total 
    }

    return render(request,'store/cart.html', context)



def remove_cart_item(request, product_id, cart_item_id):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

