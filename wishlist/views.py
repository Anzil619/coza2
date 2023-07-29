
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Product
from wishlist.models import Wishlist

# Create your views here.

@login_required(login_url='user_login')
def wishlist(request):
    user=request.user
    try:
        wishlist = Wishlist.objects.filter(user=user)
    except:
        wishlist= ''

    return render(request, 'wishlist.html',{'wishlist' : wishlist})

    

def addWishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id =int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            print(prod_id,'sifan')
            if(product_check):
                if(Wishlist.objects.filter(user=request.user,  product_id = prod_id)):
                    return JsonResponse({'status': "Product already in wishlist"})
                else:                                                

                    Wishlist.objects.create(user=request.user, product_id = prod_id)
                    return JsonResponse({'status': "product added to wishlist"})
            else:
                return JsonResponse({'status': "No such products found"})
        else:
            return JsonResponse({'status' : "Login to continue"})
    return redirect('/')



def deletewishlist(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        wishlist = Wishlist.objects.filter(user=request.user, product_id=prod_id)
        if wishlist.exists():
            wishlist.delete()
            return JsonResponse({'status': "Product removed from wishlist"})
    return redirect('wishlist')
