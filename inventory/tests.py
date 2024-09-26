from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)
class ItemAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='john_cena', password='password123')

        # Need JWT token for the user
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'john_cena',
            'password': 'password123'
        }, format='json')
        
        # Store the access token for subsequent requests
        self.token = response.data['access']
        
        # Include the token in the Authorization header for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # sample item for testing
        self.item = Item.objects.create(name="Test Item", description="Test Desc")

    def test_create_item_success(self):
        url = reverse('create_item')
        logger.warning(url)
        data = {'name': 'New Item', 'description': 'New Desc'}
        response = self.client.post(url, data, format='json')
        logger.info(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_item_already_exists(self):
        url = reverse('create_item')
        data = {'name': 'Test Item', 'description': 'Test Desc'}  # Same name as existing item
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_item_success(self):
        url = reverse('item_detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item_not_found(self):
        url = reverse('item_detail', args=[999])  # Non-existent item ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item_success(self):
        url = reverse('item_detail', args=[self.item.id])
        data = {'name': 'Updated Item', 'description': 'Updated Desc'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item_not_found(self):
        url = reverse('item_detail', args=[999])  # Non-existent item ID
        data = {'name': 'Updated Item', 'description': 'Updated Desc',}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_success(self):
        url = reverse('item_detail', args=[self.item.id])
        logger.warn(url)
        response = self.client.delete(url)
        logger.warning(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_item_not_found(self):
        url = reverse('item_detail', args=[999])  # Non-existent item ID
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
