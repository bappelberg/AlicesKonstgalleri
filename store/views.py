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
    return render(request, 'index.html')


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

