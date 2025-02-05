import json
from django.test import TestCase
from django.urls import reverse


# Create your tests here.


class GamoDjangoTest_Backend_Connect4(TestCase):

    def test_running(self):
        response = self.client.get(reverse('connect4_home'))  # URL mapped to connect4_home
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)  # check for any response

    def test_agents_list(self):
        response = self.client.get(reverse('connect4_agents'))  # URL mapped to connect4_agents
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data_dict.get("agents"))  # check that agents exist
    
    def test_start_game(self):
        response = self.client.post(reverse('connect4_start'),\
                                    json.dumps({'player-1': "Human", 'player-2': "Human"}),\
                                    content_type='application/json')
        data_dict = json.loads(response.content.decode('utf-8'))
        print(data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.client.post(reverse('connect4_start'), json.dumps({'player-1': "Human", 'player-2': "Random Agent"}), content_type='application/json')
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.client.post(reverse('connect4_start'), json.dumps({'player-1': "Random Agent", 'player-2': "Human"}), content_type='application/json')
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
    def test_get_state(self):
        self.client.post(reverse('connect4_start'), json.dumps({'player-1': "Human", 'player-2': "Human"}), content_type='application/json')
        response = self.client.get(reverse('connect4_state'))  # URL mapped to connect4_state
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertIsInstance(data_dict["state"]['board'], list)
        self.assertIsNotNone(data_dict.get("moves"))
        self.assertIsInstance(data_dict["moves"], list)
    
    def test_apply_move(self):
        self.client.post(reverse('connect4_start'), json.dumps({'player-1': "Human", 'player-2': "Human"}), content_type='application/json')
        response = self.client.post(reverse('connect4_applymove'), json.dumps({"column": 1, "player-id": 1, "is-bot": False}), content_type='application/json')
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.client.get(reverse('connect4_state'))
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertEqual(data_dict["state"]["board"][-1][0], 1.0)
        
        # check that move from bots gets applied
        self.client.post(reverse('connect4_start'), json.dumps({'player-1': "Random Agent", 'player-2': "Human"}), content_type='application/json')
        response = self.client.post(reverse('connect4_applymove'), json.dumps({"column": 1, "player-id": 1, "is-bot": True}), content_type='application/json')
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.client.get(reverse('connect4_state'))
        data_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))