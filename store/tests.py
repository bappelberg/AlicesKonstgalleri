from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from store.models import Customer


class StoreUrlsTest(TestCase):


    def test_store_url(self):
        """Test if the store page is correctly routed"""
        url = reverse('store')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        """Test if the login page is correctly routed"""
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        """Test if the logout page is correctly routed"""
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # It should redirect

    def test_orders_url(self):
        """Test if the orders page is correctly routed"""
        url = reverse('orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        """Test if the signup page is correctly routed"""
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class SignupViewTests(TestCase):

    def setUp(self):
        self.existing_customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            phone='0701234567',
            email='johndoe@example.com',
            password='password123'
        )

    def test_signup_success(self):
        response = self.client.post(reverse('signup'), {
            'firstname': 'Alice',
            'lastname': 'Johnson',
            'phone': '0709876543',
            'email': 'alice@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(email='alice@example.com').exists())

    def test_signup_invalid_email(self):
        response = self.client.post(reverse('signup'), {
            'firstname': 'Alice',
            'lastname': 'Johnson',
            'phone': '0709876543',
            'email': 'a@',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E-postadresser måste bestå av minst fem tecken')


    def test_signup_invalid_phone(self):
        response = self.client.post(reverse('signup'), {
            'firstname': 'Alice',
            'lastname': 'Johnson',
            'phone': '070123',
            'email': 'alice@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Telefonnummer måste bestå av tio siffror')

    def test_signup_invalid_password(self):
        response = self.client.post(reverse('signup'), {
            'firstname': 'Alice',
            'lastname': 'Johnson',
            'phone': '0701234567',
            'email': 'alice@example.com',
            'password': '123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lösenord måste bestå av minst fem tecken')

    def test_signup_missing_first_name(self):
        response = self.client.post(reverse('signup'), {
            'firstname': '',  # Tomt förnamn
            'lastname': 'Johnson',
            'phone': '0701234567',
            'email': 'alice@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vänligen ange förnamn')

    def test_signup_missing_last_name(self):
        response = self.client.post(reverse('signup'), {
            'firstname': 'Alice',
            'lastname': '',
            'phone': '0701234567',
            'email': 'alice@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vänligen ange efternamn')

    def test_signup_missing_password(self):
        response = self.client.post(reverse('signup'), {
            'firstname': 'Alice',
            'lastname': 'Johnson',
            'phone': '0701234567',
            'email': 'alice@example.com',
            'password': ''
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lösenord måste bestå av minst fem tecken')


class LoginViewTests(TestCase):

    def setUp(self):
        # Create a test user in the database
        self.customer = Customer.objects.create(
            first_name='Markus',
            last_name='Appelberg',
            email='markus.appelberg@example.com',
            phone='1234567890',
            password=make_password('securepassword')
        )

    def test_login_page_status_code(self):
        # Test that the login page loads correctly
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


    def test_login_with_invalid_email(self):
        # Test login with an invalid email address
        response = self.client.post(reverse('login'), data={
            'email': 'invalid.email@example.com',
            'password': 'securepassword'
        })
        self.assertContains(response, 'Invalid email!')  # Error message displayed
        self.assertNotIn('_auth_user_id', self.client.session)  # Ensure user is not logged in

    def test_login_with_invalid_password(self):
        # Test login with an invalid password
        response = self.client.post(reverse('login'), data={
            'email': 'markus.appelberg@example.com',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Invalid password!')  # Error message displayed
        self.assertNotIn('_auth_user_id', self.client.session)  # Ensure user is not logged in


    def test_error_message_display_on_failed_login(self):
        # Test that an error message is shown when login fails
        response = self.client.post(reverse('login'), data={
            'email': 'invalid.email@example.com',
            'password': 'wrongpassword'
        })
        self.assertContains(response, 'Invalid email!')  # Ensure error message is displayed

    def test_login_template_used(self):
        # Test that the correct template is used when rendering the login page
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')

    def tearDown(self):
        # Clean up any data after each test
        self.customer.delete()
