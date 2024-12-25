# Art Gallery Web Application

This is a Django-based web application for an art gallery that allows users to browse, order, and purchase products such as art pieces. It includes features such as user authentication, shopping cart, checkout, order tracking, and category-based product filtering. Below is an overview of the key components of the application.

## Features

- **Product Browsing**: Users can view and filter products based on categories (such as paintings, bracelets, etc.).
- **Shopping Cart**: Users can add products to their cart, adjust quantities, and remove items.
- **User Authentication**: The application supports user registration, login, and logout.
- **Checkout**: Users can checkout their cart, providing an address and phone number for order processing.
- **Order Management**: Users can view their past orders after logging in.

## Requirements

- Python 3.13.1
- Django 5.14 or higher
- Database: SQLite (or another supported database)
- HTML/CSS for frontend (templates)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/bappelberg/AlicesKonstgalleri
   cd AlicesKonstgalleri


2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt

3. **Setup Database**:

   ```bash
   python manage.py migrate


4. **Create a Superuser**:

   ```bash
   python manage.py createsuperuser

5. **Create a Superuser**:

   ```bash
   python manage.py runserver
