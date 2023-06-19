from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from category.models import Category
from store.models import Product

from django.db.models import Q


# Create your views here.


def homepage(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request,'home.html',context)




def search1(request):
    categories = Category.objects.all()
    products = None
       
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('is_available').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        else:
           return redirect('store')    
            
    context = {
        'products': products,
        'categories':categories,

    }
    return render(request, 'store/all_products.html', context)


def error_404_view(request, exception):
    return render(request, 'extras/404page.html' )