from django.urls import path
from . import views

urlpatterns = [

    path('', views.wishlist,name='wishlist'),
    path('addWishlist/', views.addWishlist,name='addWishlist'),
    path('deletewishlist/', views.deletewishlist,name='deletewishlist'),
   
   
]
