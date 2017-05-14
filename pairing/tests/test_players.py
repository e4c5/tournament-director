from rest_framework import status
from rest_framework.test import APITestCase
from pairing.models import Player

class PlayerTests(APITestCase):
    
    def test_create(self):
        response = self.client.post('/api/players/',{'name':'a','rating': 'b'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.post('/api/players/',{'name':'a','rating': '100'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Player.objects.filter(name='a').count(),1)
        
    def test_update(self):
        
        response = self.client.post('/api/players/',{'name':'a','rating': '100'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.put('/api/players/1/',{'name':'b','rating': '200'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Player.objects.filter(name='b').count(),1)
        self.assertEqual(Player.objects.filter(name='a').count(),0)
        
    def test_remove(self):
        response = self.client.post('/api/players/',{'name':'a','rating': '100'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.delete('/api/players/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.count(),0)
        
    
