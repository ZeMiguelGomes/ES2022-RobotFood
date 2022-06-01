from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.getFoodItems, name='getFoodItems'),
    path('uploadphoto/', views.uploadPhoto, name='uploadPhoto'),
    path('submitorder/', views.submitOrder, name='submitOrder'),
    path('orderprice/', views.orderPrice, name='orderPrice'),
]