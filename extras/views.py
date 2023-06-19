from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact_us

# Create your views here.


# Contact Us
def contact_us(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('msg')

        if email=="" or message=="":
            messages.error(request,"name or message field are empty")
            return redirect('contact_us')
        
        contact_us = Contact_us.objects.create(email=email,text=message)
        contact_us.save()
        messages.success(request,"Your feedback has been succesfully registered")
        return redirect('contact_us')
    return render(request,'extras/contact.html')



def admin_contact(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    contact = Contact_us.objects.all()
    context = {
        'contact':contact,
    }
    return render(request,'extras/contact.html',context)

def about(request):
    return render(request,'extras/about.html')

def blog(request):
    return render(request,'extras/blog.html')

def blog_detail(request):
    return render(request,'extras/blog_detail.html')
