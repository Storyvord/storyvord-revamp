from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from ..serializers.serializers_v2 import V2RegisterSerializer, V2LoginSerializer
from django.core import mail

class AuthViewsTests(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register-v2')
        self.login_url = reverse('login-v2')

    def test_register_user_success(self):
        """
        Test successful user registration and email verification.
        """
        user_data = {
            "email": "testuser@example.com",
            "password": "testpass123",
            "confirm_password":"testpass123",
            "terms_accepted":"true"
        }
        response = self.client.post(self.register_url, user_data, format='json')

        # Check that the response is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("User created successfully", response.data["message"])
        self.assertEqual(User.objects.count(), 1)  # Ensure the user is created
        self.assertEqual(User.objects.get().email, "testuser@example.com")
        # self.assertEqual(len(mail.outbox), 1)  # Ensure an email was sent

    def test_register_user_failure(self):
        """
        Test registration with missing fields.
        """
        user_data = {
            "password": "testpass123",  # Missing email
        }
        response = self.client.post(self.register_url, user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data, {
            "status": 409,
            "message": {
                "email": [
                    "This field is required."
                ],
                "confirm_password": [
                    "This field is required."
                ],
                "terms_accepted": [
                    "This field is required."
                ]
            },
            "data": None
        })

    def test_login_user_success(self):
        """
        Test successful user login.
        """
        User.objects.create_user(email="testuser@example.com", password="testpass123", verified=True)
        
        login_data = {
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("User logged in successfully", response.data["message"])
        self.assertIn("access_token", response.data["data"])
        self.assertIn("refresh_token", response.data["data"])

    def test_login_user_email_not_verified(self):
        """
        Test login for a user whose email is not verified.
        """
        user = User.objects.create_user(email="testuser@example.com", password="testpass123")
        user.verified = False  # Simulate that the user is not verified
        user.save()

        login_data = {
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email is not verified. A verification email has been sent.", response.data["message"])
        # self.assertEqual(len(mail.outbox), 1)  # Ensure an email was sent

    def test_login_user_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        User.objects.create_user(email="testuser@example.com", password="testpass123", verified=True)

        login_data = {
            "email": "testuser@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, login_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn("Invalid email or password", response.data["message"])
