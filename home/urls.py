from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage,name='homepage'),
    path('search1', views.search1,name='search1'),
    
]
