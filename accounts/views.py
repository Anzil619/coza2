

from .forms import UserRegistrationForm
from django.utils.crypto import get_random_string
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from accounts.models import CustomUser, UserOTP
from carts.models import Cart, CartItem
from django.conf import settings
from django.contrib import messages
from carts.views import _cart_id
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from .models import UserOTP
from django.contrib import messages,auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login






@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def user_login(request):
    # if 'email' in request.session:
    #     return redirect('homepage')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if email.strip() == '' or password.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('user_login')
        user = auth.authenticate(email=email, password=password)

        
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    # gettting product variation by cart_id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    # get the cart items from the user to access the product variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id_list = []

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id_list.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            
                            for item in cart_item:
                                item.user = user
                                item.save()


            except:
                pass

            request.session['email'] = email
            auth.login(request,user)
            return redirect ('homepage')
        else:
            messages.error(request, "invalid username and password")
            return render (request,'user_login.html')
        
    return render(request,'user_login.html')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def logout(request):
    # if 'email' in request.session:
    #     request.session.flush()
    auth.logout(request)
    
    return redirect('user_login')



def register(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        form = UserRegistrationForm(request.POST)

        if otp:
            email = request.POST.get('email')
            usr = CustomUser.objects.get(email=email)
            last_otp = UserOTP.objects.filter(user=usr).last()

            if int(otp) == last_otp.otp:
                usr.is_active = True
                usr.save()
                login(request, usr)
                messages.success(request, f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('homepage')
            else:
                messages.warning(request, 'You entered a wrong OTP')
                return render(request, 'user_signup.html', {'otp': True, 'usr': usr, 'form': form})
        else:
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                user_otp = get_random_string(length=6, allowed_chars='0123456789')
                UserOTP.objects.create(user=user, otp=user_otp)

                email_subject = 'Welcome to Coza Store, Verify Your Email'
                email_message = f'Hello {user.first_name},\n\nOTP to verify your account for Coza store is {user_otp}\n\nHappy Shopping..!!'
                send_mail(email_subject, email_message, settings.EMAIL_HOST_USER, [user.email])

                messages.success(request, 'Registration successful. Please check your email for OTP verification.')
                return render(request, 'user_signup.html', {'otp': True, 'usr': user, 'form': form})
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field.capitalize()}: {error}')

    else:
        form = UserRegistrationForm()

    return render(request, 'user_signup.html', {'form': form})



