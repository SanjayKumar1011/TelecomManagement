from django.test import TestCase
from .models import User
from rest_framework.test import APITestCase
from django.urls import reverse

class UserModelTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin1', password='adminpass', role='admin')
        self.customer_user = User.objects.create_user(username='cust1', password='custpass', role='customer')
        self.employee_user = User.objects.create_user(username='emp1', password='emppass', role='employee')

    def test_user_creation(self):
        self.assertEqual(self.admin_user.username, 'admin1')
        self.assertTrue(self.admin_user.check_password('adminpass'))
        self.assertEqual(self.admin_user.role, 'admin')

        self.assertEqual(self.customer_user.role, 'customer')
        self.assertEqual(self.employee_user.role, 'employee')

    def test_user_str_method(self):
        self.assertEqual(str(self.admin_user), "admin1 (admin)")
        self.assertEqual(str(self.customer_user), "cust1 (customer)")


class AuthPermissionTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', role='admin')
        self.customer_user = User.objects.create_user(username='customer', password='custpass', role='customer')
        self.login_url = reverse('login')  # JWT login endpoint

    def get_token(self, username, password):
        response = self.client.post(self.login_url, {'username': username, 'password': password}, format='json')
        return response.data['access']

    def test_admin_login(self):
        token = self.get_token('admin', 'adminpass')
        self.assertIsNotNone(token)

    def test_customer_login(self):
        token = self.get_token('customer', 'custpass')
        self.assertIsNotNone(token)