from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< Updated upstream
=======
    path('login/', views.loginStaff, name='loginStaff'),
    path('getOrder/', views.getOrders, name='getOrder'),

>>>>>>> Stashed changes
]