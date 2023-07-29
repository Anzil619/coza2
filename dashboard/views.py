
from datetime import datetime, timedelta
import re
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from userprofile.models import Address
from order.models import Order, OrderItem
from store.models import Product, Variation,PriceFilter,ProductOffer
from category.models import Category,Sub_Category
from django.db.models.functions import TruncDay,Cast
from order.models import Coupon
from django.db.models import Sum,DateField
from accounts.models import CustomUser

# Create your views here.
def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_superuser:
            request.session['email'] = email
            auth.login(request, user)
            print('admin logged in ')
            messages.success(request, 'successfully signed up!')
            return redirect('dashboard')
        else:
            print('Not autherised')
            messages.error(request, 'Not autherised')
            return redirect('adminlogin')
        
    return render(request, 'dashboard/adminlogin.html')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='adminlogin')
# Create your views here.
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('adminlogin')

    delivered_items = OrderItem.objects.filter(status='Delivered')

    revenue = 0
    for item in delivered_items:
        revenue += item.order.total_price

    top_selling = OrderItem.objects.annotate(total_quantity= Sum('quantity')).order_by('-total_quantity').distinct()[:5]

    recent_sale = OrderItem.objects.all().order_by('-id')[:5]

    today = datetime.today()
    date_range = 7

    four_days_ago = today - timedelta(days=date_range)

    # orders = Order.objects.filter(created_at_gte=four_days_ago, created_at_lte=today)
    orders = Order.objects.filter(created_at__gte=four_days_ago, created_at__lte=today)
    sales_by_day = orders.annotate(day=TruncDay('created_at')).values('day').annotate(total_sales=Sum('total_price')).order_by('day')
    print(sales_by_day,"daxii")
    sales_dates = Order.objects.annotate(sale_date=Cast('created_at', output_field=DateField())).values('sale_date').distinct()

    context = {
        'total_users':CustomUser.objects.count(),
        'sales':OrderItem.objects.count(),
        'revenue':revenue,
        'top_selling':top_selling,
        'recent_sales':recent_sale,
        'sales_by_day':sales_by_day,
    }
    return render(request,'dashboard/admin_home.html',context)



def users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render (request,'dashboard/users.html',context)


def blockuser(request,id):
    user = CustomUser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request,'user successfully blocked')
    else:
        user.is_active = True
        user.save()
        messages.success(request,'user successfully unblocked')
    return redirect('users')



def adminlogout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect('adminlogin')


def product_list(request):
    if 'email' in request.session:
        products = Product.objects.all()
        categories = Category.objects.all()
        sub_categories = Sub_Category.objects.all()
        offer =  ProductOffer.objects.all()
        price_range = PriceFilter.objects.all()
        print(price_range,"daxo")
        
        context = {
            'products' : products,
            'category' : categories,
            'sub_category' : sub_categories,
            'offer' : offer,
            'price_range' : price_range,
        }
        return render(request, 'dashboard/product_list.html',context)
    else:
        return redirect('adminlogin')


def product_delete(request, id):
    products = Product.objects.filter(id=id)
    products.delete()
    return redirect('product_list')


def add_product(request):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()
    offer =  ProductOffer.objects.all()
    price_range = PriceFilter.objects.all()
    
    context = {
            'category' : categories,
            'sub_category' : sub_categories,
            'offer'        : offer,
            'price_range'  : price_range,
        }
    
    if request.method == "POST":
        product_name = request.POST['product_name']
        stock = request.POST['stock']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES.get('image', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3',None)
        category = request.POST.get('category')
        offer_name  = request.POST.get('offer')
        price_ranges  = request.POST.get('price_range')
        print(category,'sifan')
        sub_category = request.POST.get('sub_category')

        # validation product already exist


        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request, 'Product name already exist')
            return redirect('product_list')
        

        if product_name == '':
            messages.error(request,"name field are empty")
            return redirect('product_list')
        
        
        if not re.search('[a-zA-Z]', product_name):
            messages.error(request, 'Product name should contain at least one alphabet')
            return redirect('product_list')
        

        try:
            check_number = int(price)
            check_number = int(stock)
        except:
            messages.info(request,'number field got unexpected values')
            return redirect('product_list')
        
        #validation for product price and stock less than zero

        check_pos =[int(price),int(stock)]
        for value in check_pos:
            if value < 0 or value == '':
                messages.info(request,'price and quantity should be positive number')
                return redirect('product_list')
            else:
                pass

        
        if image is None or image1 is None or image2 is None or image3 is None:
            messages.error(request, 'Image field is empty.')
            return redirect('product_list')


        try:
            cat = Category.objects.get(category_name=category)
        except Category.DoesNotExist:

    # Handle the case when the category does not exist
            messages.error(request, 'Invalid category')
            return redirect('product_list')

        try:
           sub_cate = Sub_Category.objects.get(sub_category_name=sub_category)
        except Sub_Category.DoesNotExist:

    # Handle the case when the sub-category does not exist
            messages.error(request, 'Invalid sub-category')
            return redirect('product_list')
        

        price_range = PriceFilter.objects.get(price_range=price_ranges)

        new = Product.objects.create(
                product_name=product_name,
                stock=stock,
                price=price,
                images=image,
                image1=image1,
                image2=image2,
                image3=image3,
                category=cat,
                sub_category=sub_cate,
                description=description,
                price_range = price_range,
                
        )

        try:
            offers=ProductOffer.objects.get(offer_name=offer_name)
            new.offer = offers
            new.save()
        except:
            pass


        new.is_available=True
        new.save()

        return redirect('product_list')
    
    return render(request, 'dashboard/product_list.html',context)

    



def product_edit(request, product_id):
    categories = Category.objects.all()
    sub_categories = Sub_Category.objects.all()
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product_name = request.POST.get('product_name')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        offer_name  = request.POST.get('offer')
        price_ranges  = request.POST.get('price_range')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')

        if Product.objects.filter(product_name=product_name).exclude(id=product_id).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product_list')

        if not (product_name and price):
            messages.error(request, "Name or price field is empty")
            return redirect('product_list')

        if not re.search('[a-zA-Z]', product_name):
            messages.error(request, 'Product name should contain at least one alphabet')
            return redirect('product_list')
        
        try:
            check_number = int(price)
            check_number = int(stock)
        except:
            messages.info(request,'number field got unexpected values')
            return redirect('product_list')
        
        check_pos =[int(price),int(stock)]
        for value in check_pos:
            if value < 0 or value == '':
                messages.info(request,'price and quantity should be positive number')
                return redirect('product_list')
            else:
                pass
        
        
        cat = get_object_or_404(Category, category_name=category)
        sub_cate = get_object_or_404(Sub_Category, sub_category_name=sub_category)
        price_range = PriceFilter.objects.get(price_range=price_ranges)

        product.product_name = product_name
        product.stock = stock
        product.price = price
        product.description = description
        product.category = cat
        product.sub_category = sub_cate
        product.price_range = price_range
        product.is_available = True

        try:
            offers=ProductOffer.objects.get(offer_name=offer_name)
            product.offer = offers
        except:
            pass
        
        if image:
            product.images = image
        if image1:
            product.image1 = image1
        if image2:
            product.image2 = image2
        if image3:
            product.image3 = image3

        product.save()

        return redirect('product_list')

    context = {
        'category': categories,
        'sub_category': sub_categories,
        'product': product,
    }

    return render(request, 'dashboard/product_list.html', context)




def category_list(request):
    category = Category.objects.all()
    context={
        'category' : category
    }

    return render(request, 'dashboard/category_list.html',context)


def add_category(request):
    if request.method == "POST":
        category_name = request.POST['category_name']
        description = request.POST['description']
        
        if Category.objects.filter(category_name=category_name).exists():
            messages.error(request, 'Category name already exist')
            return redirect('category_list')
        

        if category_name == '':
            messages.error(request,"name or slug field are empty")
            return redirect('category_list')
        
        if not re.search('[a-zA-Z]', category_name):
            messages.error(request, 'category name should contain at least one alphabet')
            return redirect('category_list')
            
        

        new = Category.objects.create(
                category_name=category_name,
        
                description=description
        )

        new.save()

        return redirect('category_list')
    

    return render(request, 'dashboard/category_list.html')


def category_delete(request, category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_list')

def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        
        print(category_name)

        if Category.objects.filter(category_name=category_name).exclude(id=category_id).exists():
            messages.error(request, 'Product name already exists')
            return redirect('add_product')
        
        if category_name == '':
            messages.error(request,"name or slug field are empty")
            return redirect('category_list')
        
        if not re.search('[a-zA-Z]', category_name):
            messages.error(request, 'category name should contain at least one alphabet')
            return redirect('category_list')
        

        category.category_name = category_name
        category.description = description
        category.save()

        return redirect('category_list')

    
    return render(request, 'dashboard/category_list.html')
    
    
def sub_category_list(request):
    sub = Sub_Category.objects.all()
    cat = Category.objects.all()
    context = {

        'sub_category' : sub,
        'category' : cat,

    }
    return render(request, 'dashboard/sub_category_list.html',context)


def add_sub_category(request):
    if request.method == "POST":
        sub_category_name = request.POST['sub_category_name']
        category_name = request.POST['category']

        
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exists():
            messages.error(request, 'Sub Category name already exist')
            return redirect('sub_category_list')
        

        if sub_category_name == '':
            messages.error(request,"name field are empty")
            return redirect('sub_category_list')
        
        
        
        if not re.search('[a-zA-Z]', sub_category_name):
            messages.error(request, 'sub category name should contain at least one alphabet')
            return redirect('sub_category_list')
        

        category = Category.objects.get(category_name=category_name)
        
        new = Sub_Category.objects.create(
                sub_category_name=sub_category_name,
        
                category=category
        )

        new.save()

        return redirect('sub_category_list')
    

    return render(request, 'dashboard/sub_category_list.html')


def sub_category_delete(request,sub_id):
    sub= Sub_Category.objects.get(id=sub_id)
    sub.delete()
    return redirect('sub_category_list')

def sub_category_edit(request,sub_id):
    sub_category = Sub_Category.objects.get(id=sub_id)

    if request.method == "POST":
        sub_category_name = request.POST.get('sub_category_name')
        
        
        category_name = request.POST.get('category')
        
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exclude(id=sub_id).exists():
            messages.error(request, 'sub category name already exists')
            return redirect('sub_category_list')

        # if not (category_name):
        #     messages.error(request, "Name  field is empty")
        #     return redirect('product_list')
        

        category = Category.objects.get(category_name=category_name)
        
        sub_category.sub_category_name = sub_category_name
        sub_category.category = category
        
        
        sub_category.save()

        return redirect('sub_category_list')

    
    return render(request, 'dashboard/sub_category_list.html')


def order_management(request):
    order_items = OrderItem.objects.all()
    order = Order.objects.all()


    context = {
        'orders' : order,
    }

    return render(request, 'dashboard/admin_order_list.html',context)

def admin_single_order(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return redirect('order_management')
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

    return render (request, 'dashboard/single_order_admin.html', context)


def update_order(request, id):
  if request.method == "POST":
    order_item = get_object_or_404(OrderItem, id=id)
    status = request.POST.get('status')
    order_item.status = status 
    order_item.save()
    
    return redirect('admin_single_order',id)

    

def coupon_management(request):
    coupon = Coupon.objects.all()

    context = {
        'coupon' : coupon
    }
    return render(request, 'dashboard/admin_coupon.html',context)


def add_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        valid_till = request.POST.get('valid_till')
        is_available = request.POST.get('is_available')

        if is_available == None:
            is_available = False

        if int(discount) >30 or int(discount) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('coupon_management')


        Coupon.objects.create(
            code=coupon_code,
            discount=discount,
            min_value=min_value,
            valid_till=valid_till,
            active = is_available,
        )

        return redirect('coupon_management')
    

def edit_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_value = request.POST.get('min_value')
        valid_till = request.POST.get('valid_till')
        is_available = request.POST.get('is_available')


        if is_available == None:
            is_available = False
        
        if valid_till =="":
            valid_till = coupon.valid_till

        if int(discount) >30 or int(discount) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('offer_managment')
        
        coupon.code = coupon_code
        coupon.discount = discount
        coupon.min_value = min_value
        coupon.valid_till = valid_till
        coupon.active = is_available
        coupon.save()
        return redirect('coupon_management')
    
def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('coupon_management')
    
def variants(request):
    variant = Variation.objects.all()
    product = Product.objects.all()
    variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),)   
    


    context = {
        'variants' : variant,
        'products' : product,
        'choices' : variation_category_choice,

    }
    return render(request, 'dashboard/variation.html', context)

def add_variants(request):
    if request.method == "POST":
        product_name = request.POST.get('product')
        variation_category = request.POST.get('variation_category')
        variation_value = request.POST.get('variation_value')
        is_available = request.POST.get('is_available')
        print(variation_value,"daxo")
        product = Product.objects.get(product_name=product_name)
        if is_available == None:
            is_available = False

        Variation.objects.create(product=product, variation_category=variation_category,variation_value=variation_value,is_active=is_available)


        return redirect('variants')
    





def delete_variants(request, id):
    variants = Variation.objects.get(id=id)
    variants.delete()
    return redirect('variants')

def price_range(request):
    choices = PriceFilter.FILTER_CHOICES
    price_range=PriceFilter.objects.all()
    

    context ={
        'price_range' : price_range,
        'choices' : choices,
    }

    return render(request,'dashboard/price_range.html',context)

def add_price_range(request):
    if request.method == 'POST':
        price_range = request.POST.get('price_range')

        if PriceFilter.objects.filter(price_range=price_range).exists():
            messages.error(request, 'price range already exists')
            return redirect('price_range')
        
        PriceFilter.objects.create(price_range=price_range)
    return redirect('price_range')


def delete_price_range(request,id):
    price_range = PriceFilter.objects.get(id=id)
    price_range.delete()
    return redirect('price_range')

def edit_price_range(request,id):
    price_rangee = PriceFilter.objects.get(id=id)
    if request.method == "POST":
        price_ranges = request.POST.get('price_range')

        if PriceFilter.objects.filter(price_range=price_ranges).exclude(id=id).exists():
            messages.error(request,"price range already exist")
            return redirect(price_range)
        
        price_rangee.price_range = price_ranges
        price_rangee.save()
        return redirect('price_range')
    
def offer_managment(request):
    offer = ProductOffer.objects.all()
    context ={
        'offer' : offer
    }
    return render(request, 'dashboard/offer_managment.html',context)
  
def add_offer(request):
    if request.method == "POST":
        offer_name = request.POST.get('offer_name')
        offer_description = request.POST.get('offer_description')
        discount = request.POST.get('offer_discount')
        valid_till = request.POST.get('valid_till')

        if ProductOffer.objects.filter(offer_name=offer_name).exists():
            messages.error(request,"offer Already exist")
            return redirect('offer_managment')

        if int(discount) >30 or int(discount) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('offer_managment')
        
        if valid_till == "":
            messages.error(request,'date field is empty')
            return redirect('offer_managment')
        
        try:
            check_number = int(discount)
        except:
            messages.info(request,'discount field got unexpected values')
            return redirect('offer_managment')

        ProductOffer.objects.create(offer_name=offer_name,offer_description=offer_description,offer_discount = discount,valid_till=valid_till)

        return redirect('offer_managment')
    
def editoffer(request,offer_id):
    offers = ProductOffer.objects.get(id=offer_id)
    if request.method == "POST":
        offer_names = request.POST.get('offer_name')
        offer_descriptions = request.POST.get('offer_description')
        offer_discounts = request.POST.get('offer_discount')
       
        valid_till = request.POST.get('valid_till')

        if valid_till == "":
            valid_till=offers.valid_till

        if int(offer_discounts) >30 or int(offer_discounts) <= 0 :
            messages.error(request,"discount percentage should be below 30 percentage and more than zero")
            return redirect('offer_managment')
        

        offers.offer_name = offer_names
        offers.offer_discount =   offer_discounts
        offers.offer_description = offer_descriptions
        offers.valid_till = valid_till
        offers.save()
        return redirect('offer_managment')

def delete_offer(request,id):
    offer = ProductOffer.objects.get(id=id)
    offer.delete()
    return redirect('offer_managment')
