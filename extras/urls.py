from django.urls import path
from . import views

urlpatterns = [
    path('contact_us/', views.contact_us,name='contact_us'),
    path('about/', views.about,name='about'),
    path('blog/', views.blog,name='blog'),
    path('blog_detail/', views.blog_detail,name='blog_detail'),
    
    
]
