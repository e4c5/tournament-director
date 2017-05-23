import random, math

from rest_framework import status
from rest_framework.test import APITestCase
from pairing.models import Player
from pairing import utils
from pairing.swiss import Pairing
from _pydecimal import InvalidOperation

class PairingTests(APITestCase):
    players = [ ['Leon Vidal',10],
                ['James Faukner',20],
                ['Norman Uris',30],
                ['Tom Ludlum',40],
                ['Jeffery Mailer',50],
                ['Louis Chrisholm',60],
                ['Ernest Harper',70],
                ['Salman Patterson',80],
                ['Alistair Higgins',90],
                ['Jack Smith',100],
                ['J.R.R Archer',110],
                ['W.E Blyton',120],
                ['Richmol Jame',130],
                ['Mario Pilcher',140],
                ['Peter Spillane',150]]

    def setUp(self):
        for player in self.players:
            Player.objects.create(name=player[0], rating=player[1])
            
        self.assertEqual(Player.objects.count(),15)
        

        
    def test_validation(self):
        self.assertFalse(utils.validate_players())
        
        Player.objects.create(name='Bye', rating=0)
        self.assertTrue(utils.validate_players())
        self.assertTrue(utils.validate_results())
        
    def test_first_round(self):
        players = []
        for player in self.players:
            players.append({'name': player[0], 'rating': player[1], 'score': 0, 'spread':0 })
            
        s = Pairing(1)
        s.players = players
        self.assertRaises(InvalidOperation)
        
        players.append({'name': 'bye', 'rating':0, 'score':0 , 'spread':0})
        self.assertEquals(len(s.pairs),0)
        s.make_it()
        self.assertEquals(len(s.pairs),8)
        
        first = s.pairs[0]
        self.assertEqual(first[0]['name'], 'bye')
        self.assertEqual(first[1]['name'], 'Leon Vidal')
        
        last = s.pairs[1]
        self.assertEqual(last[0]['name'], 'Peter Spillane')
        self.assertEqual(last[1]['name'], 'Salman Patterson')
        
        
    