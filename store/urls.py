from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('orders/', views.orders, name='orders'),
    path('signup/', views.signup, name='signup'),
    path('cart/', views.cart, name='cart'),
    path('check-out/', views.check_out, name='check-out'),
]
