from django.urls import path
from . import views

urlpatterns = [

    path('', views.store,name='store'),
    path('<slug:category_slug>/', views.store,name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:sub_category_slug>/', views.products_by_sub_category,name='products_by_sub_category'),
    path('search/', views.search, name='search'),
   
]
