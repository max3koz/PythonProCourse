from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class BookCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='pass123')

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/books/', {
            'title': 'Test Book',
            'author': 'Author1',
            'genre': 'Drama',
            'publication_year': 2022
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Test Book')
