from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models import Product, Order, Customer, Category
from django.contrib.auth.hashers import check_password, make_password


# Cart View
def cart(request):
    return render(request, 'cart.html')

# Index View
def index(request):
    return render(request, 'index.html')


# Login View
def login(request):
    return render(request, 'login.html')



# Orders View
def orders(request):
    return render(request, 'orders.html')


# Store View
def store(request):
    return render(request, 'index.html')


# Signup View
def signup(request):
    return render(request, 'signup.html')

