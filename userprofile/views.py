from django.shortcuts import redirect, render
from accounts.models import CustomUser

from userprofile.models import Address, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import editprofile
from django.contrib.auth.decorators import login_required


# Create your views here.



def add_address(request):
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        order_note = request.POST.get('ordernote')

        if request.user is None:
            return 
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First name or Last name is empty!')
            return redirect('profile')
        if country.strip() =='':
            messages.error(request, 'Country is empty!')
            return redirect('profile')
        if city.strip() =='':
            messages.error(request, 'City is empty!')
            return redirect('profile')
        if address.strip() =='':
            messages.error(request, 'Address is empty!')
            return redirect('profile')
        if pincode.strip() =='':
            messages.error(request, 'Pincode is empty!')
            return redirect('profile')
        if phone.strip() =='':
            messages.error(request, 'Phone is empty!')
            return redirect('profile')
        if email.strip() =='':
            messages.error(request, 'Email is empty!')
            return redirect('profile')
        if state.strip() =='':
            messages.error(request, 'State is empty!')
            return redirect('profile')
        
        adrs = Address()
        adrs.user = request.user
        adrs.first_name = first_name
        adrs.last_name = last_name
        adrs.country = country
        adrs.address = address
        adrs.city = city
        adrs.pincode = pincode
        adrs.phone = phone
        adrs.email = email
        adrs.state = state
        adrs.order_note = order_note
        adrs.save()
       
        return redirect('checkout')
    
    return render(request, 'store/checkout.html')

def addaddress_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        order_note = request.POST.get('ordernote')

        if request.user is None:
            return 
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First name or Last name is empty!')
            return redirect('profile')
        if country.strip() =='':
            messages.error(request, 'Country is empty!')
            return redirect('profile')
        if city.strip() =='':
            messages.error(request, 'City is empty!')
            return redirect('profile')
        if address.strip() =='':
            messages.error(request, 'Address is empty!')
            return redirect('profile')
        if pincode.strip() =='':
            messages.error(request, 'Pincode is empty!')
            return redirect('profile')
        if phone.strip() =='':
            messages.error(request, 'Phone is empty!')
            return redirect('profile')
        if email.strip() =='':
            messages.error(request, 'Email is empty!')
            return redirect('profile')
        if state.strip() =='':
            messages.error(request, 'State is empty!')
            return redirect('profile')
        
        adrs = Address()
        adrs.user = request.user
        adrs.first_name = first_name
        adrs.last_name = last_name
        adrs.country = country
        adrs.address = address
        adrs.city = city
        adrs.pincode = pincode
        adrs.phone = phone
        adrs.email = email
        adrs.state = state
        adrs.order_note = order_note
        adrs.save()

        return redirect('profile')


def delete_address(request, address_id):
    
    address =Address.objects.filter(id=address_id)
    address.delete()
    return redirect('checkout')

def deleteaddress_profile(request,delete_id):
    address = Address.objects.get(id = delete_id)
    address.delete()
    return redirect('profile')

def profile(request):
    user = request.user
    address = Address.objects.filter(user=user)
    # wallet_balance = Wallet.objects.get(user = user)
    context ={
        'address' : address,
        # 'wallet' : wallet_balance,
    }
    return render(request, 'userprofile/profile_details.html',context)


def editprofiles(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Validation
        if username == '':
            messages.error(request, 'Username is empty')
            return redirect('profile')
        if first_name == '' or last_name == '':
            messages.error(request, 'First or Lastname is empty')
            return redirect('profile')

        try:
            user = CustomUser.objects.get(email=request.user)
            print(user)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.save()
        except ObjectDoesNotExist:
            messages.error(request, 'User does not exist')
        return redirect('profile')

    
  
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent the user from being logged out
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('profile')  # Replace 'home' with the appropriate URL name for your home page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'userprofile/profile_details.html', {'form': form})


    
    

        
    





