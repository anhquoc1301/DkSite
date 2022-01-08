from django.urls import path
from .views import *
urlpatterns = [
    path('login_register/', login_register, name='login_register'),
    path('logout/', logout,name= 'logout'),
    path('', home, name='home'),
    path('my_product/', my_product, name='my_product'),
    path('cart/<str:pk>/', cart, name='cart'),
    path('waitaccept/', waitaccept1, name='waitaccept'),
    path('success/<str:pk>/', success,name= 'success'),
    path('cancel/<str:pk>/', cancel, name='cancel'),
    path('addproduct/', addproduct, name='addproduct'),
    path('orders/',orders, name='orders'),
    path('messages/',messages, name='messages'),
    path('profile/', profile, name='profile'),

]