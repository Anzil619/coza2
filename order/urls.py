from django.urls import path, include
from .import views

urlpatterns = [

    path('', views.checkout, name='checkout'),
    path('placeorder/',views.placeorder, name='placeorder'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('ordercancel/', views.ordercancel, name='ordercancel'),
    path('order_return/<int:id>/', views.order_return, name='order_return'),
    # path('order_return/<int:id>/', views.order_return, name='order_return'),
    path('coupons/', views.coupons, name='coupons'),
    path('proceedtopay/', views.razarypaycheck, name = 'razarypaycheck'),
    path('checkout/proceed-to-pay/',views.sample),
    path('single_order_details/<int:id>/',views.single_order_details, name='single_order_details'),
    path('export_csv/',views.export_csv, name="export_csv"),
    # path('export_pdf/', views.export_pdf, name='export_pdf'),
    # path('order_success/',views.order_success, name='order_success'),
    
]