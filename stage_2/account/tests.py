from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Organisation, User

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/auth/register'
        self.login_url = '/auth/login'
        
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "johndoe@example.com",
            "password": "password123",
            "phone": "1234567890"
        }

    def test_register_user_successfully(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], self.user_data['firstName'])
        self.assertEqual(response.data['data']['user']['email'], self.user_data['email'])
        
        # Verify default organisation
        org_name = f"{self.user_data['firstName']}'s Organisation"
        self.assertTrue(Organisation.objects.filter(name=org_name).exists())

    def test_login_user_successfully(self):
        # First, register the user
        self.client.post(self.register_url, self.user_data, format='json')
        
        login_data = {
            "email": self.user_data['email'],
            "password": self.user_data['password']
        }
        
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['email'], self.user_data['email'])

    def test_register_fails_missing_fields(self):
        missing_fields_data = [
            {**self.user_data, "firstName": ""},
            {**self.user_data, "lastName": ""},
            {**self.user_data, "email": ""},
            {**self.user_data, "password": ""}
        ]
        
        for data in missing_fields_data:
            response = self.client.post(self.register_url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
            self.assertIn('errors', response.data)

    def test_register_fails_duplicate_email(self):
        # Register the first user
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Try to register a second user with the same email
        duplicate_email_data = {**self.user_data, "firstName": "Jane"}
        response = self.client.post(self.register_url, duplicate_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('errors', response.data)

if __name__ == "__main__":
    TestCase.main()
