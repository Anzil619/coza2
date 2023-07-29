
from django.shortcuts import render, redirect,get_object_or_404
from category.models import Category, Sub_Category
from carts.views import _cart_id
from carts.models import CartItem
from store.models import PriceFilter, Product
from django.db.models import Q
from django.core.paginator import Paginator



# Create your views here.

def store(request, category_slug=None):
    categories = None
    products   = None
    sub_category = Sub_Category.objects.all()
    sub_category_id = request.GET.get('sub_category_id')
    filter_prices = PriceFilter.objects.all()
    filter_price_id = request.GET.get('filter_price')
    sort = request.GET.get('sort')



    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products   = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
    elif sub_category_id:
        products = Product.objects.filter(sub_category__id=sub_category_id)
        paginator = Paginator(products, 3)

    elif filter_price_id:
        products = Product.objects.filter(price_range=filter_price_id)
        paginator = Paginator(products, 3)
    elif sort == 'atoz':
        products = Product.objects.order_by('product_name')
        paginator = Paginator(products, 3)
     
    elif sort == 'ztoa':
        products = Product.objects.order_by('-product_name')
        paginator = Paginator(products, 3)

    elif sort == 'ltoh':
        products = Product.objects.order_by('price')
        paginator = Paginator(products, 3)

    elif sort == 'htol':
        products = Product.objects.order_by('-price')
        paginator = Paginator(products, 3)
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)


    context = {
        'products' : paged_products,
        'filter_prices' : filter_prices,    
        'sub_category' : sub_category,   
    }

    return render(request,'store/all_products.html',context)


def product_detail(request, category_slug , product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    
    context={
        "single_product" : single_product,
        'in_cart' : in_cart
    }

    return render(request, 'store/product_detail.html', context)




def search(request):
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


