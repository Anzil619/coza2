from . import views
from django.urls import path


urlpatterns = [
    path('add_address/', views.add_address, name='add_address'),
    path('profile/', views.profile, name='profile'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('editprofiles/', views.editprofiles, name='editprofiles'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('addaddress_profile/', views.addaddress_profile, name='addaddress_profile'),
    path('deleteaddress_profile/<int:delete_id>/', views.deleteaddress_profile, name='deleteaddress_profile'),
    

]