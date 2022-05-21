from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginStaff, name='loginStaff'),
    path('getOrder/', views.getOrders, name='getOrder'),
    path('login/', views.loginStaff, name='loginStaff'),
]