from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class TokenFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(username='owner', password='secret123', email='owner@example.com')

    def test_token_project_and_logout(self):
        self.assertEqual(self.client.get('/api/v1/projects/').status_code, 200)
        payload = {'title': 'Demo', 'description': 'Test', 'tech_stack': 'Dart', 'url_link': 'https://example.com', 'image': ''}
        self.assertEqual(self.client.post('/api/v1/projects/', payload, format='json').status_code, 401)
        login = self.client.post('/api/v1/auth/token/', {'username': 'owner', 'password': 'secret123'}, format='json')
        self.assertEqual(login.status_code, 200)
        token = login.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        created = self.client.post('/api/v1/projects/', payload, format='json')
        self.assertEqual(created.status_code, 201, created.data)
        self.assertEqual(created.data['url_link'], payload['url_link'])
        self.assertEqual(self.client.post('/api/v1/auth/logout/').status_code, 204)
        self.assertFalse(Token.objects.filter(key=token).exists())
        self.assertEqual(self.client.post('/api/v1/projects/', payload, format='json').status_code, 401)
