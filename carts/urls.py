from . import views
from django.urls import path


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('increment_cart/', views.increment_cart, name='increment_cart'),
    # # path('checkout/', views.checkout, name='checkout'),
    
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
]