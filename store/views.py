from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models import Product, Order, Customer, Category
from django.contrib.auth.hashers import check_password, make_password


# Cart View
def cart(request):
    if request.method == 'GET':
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})

def check_out(request):
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    customer = request.session.get('customer')
    cart = request.session.get('cart')
    products = Product.get_products_by_id(list(cart.keys()))
    print(address, phone, customer, cart, products)

    for product in products:
        print(cart.get(str(product.id)))
        order = Order(customer=Customer(id=customer),
                      product=product,
                      price=product.price,
                      address=address,
                      phone=phone,
                      quantity=cart.get(str(product.id)))

        # order.save() to be implemented

    request.session['cart'] = {}

    return redirect('cart')


# Index View
def index(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('index')

    if request.method == 'GET':
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


# Login View
def login(request):
    # Retrieve the return_url if provided in the GET request
    return_url = request.GET.get('return_url')

    if request.method == 'POST':
        # Get the POST data (email and password)
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Find the customer by email
        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            # Check if the password matches
            flag = check_password(password, customer.password)
            if flag:
                # Store customer ID and first_time current in the session
                request.session['customer'] = customer.id
                request.session['first_name'] = customer.first_name

                # Redirect to return_url if provided, else to index
                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return redirect('index')
            else:
                error_message = 'Invalid password!'
        else:
            error_message = 'Invalid email!'

        # If there's an error, render the login page with the error message
        return render(request, 'login.html', {'error': error_message})

    # If the method is GET, just render the login page
    return render(request, 'login.html')


# Logout view
def logout(request):
    request.session.clear()  # Clear session to log out the user
    return redirect('login')  # Redirect to login page


# Orders View
def orders(request):
    return render(request, 'orders.html')


# Store View
def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    return render(request, 'index.html', data)


# Signup View
def signup(request):
    if request.method == 'POST':
        # Get POST-data
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate data
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )
        error_message = validate_customer(customer)

        if not error_message:
            customer.password = make_password(customer.password)  # Hash password
            customer.save()  # Save customer in database
            return redirect('index')  # If no error, redirect customer to index ingen fel, omdirigera till hemsidan
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)  # Render signup.html view error messages

    return render(request, 'signup.html')  # Render signup.html for GET method


def validate_customer(customer):
    error_message = None
    if not customer.first_name:
        error_message = "Vänligen ange förnamn"
    elif len(customer.first_name) < 3:
        error_message = 'Förnamn måste bestå av minst tre bokstäver'
    elif not customer.last_name:
        error_message = 'Vänligen ange efternamn'
    elif len(customer.last_name) < 3:
        error_message = 'Efternamn måste bestå av minst tre bokstäver'
    elif not customer.phone:
        error_message = 'Ange telefonnummer'
    elif len(customer.phone) < 10:
        error_message = 'Telefonnummer måste bestå av tio siffror'
    elif len(customer.password) < 5:
        error_message = 'Lösenord måste bestå av minst fem tecken'
    elif len(customer.email) < 5:
        error_message = 'E-postadresser måste bestå av minst fem tecken'
    elif customer.is_exists():
        error_message = 'E-postadressen finns redan registrerad i vårt system'
    return error_message
