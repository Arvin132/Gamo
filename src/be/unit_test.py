import unittest
from backend import app
import json

class GamoFlaskTest_Backend_Connect4(unittest.TestCase):

    # Setup method to configure the test environment
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_running(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.decode() != None) # check for any response
        
    def test_agents_list(self):
        response = self.app.get('/get-agents-list')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data_dict.get("agents")) # check that agents exist
        
    def test_start_game(self):
        # check for all the different possible assignments
        response = self.app.post('/start-game-connect4',\
                                    json={'player-1': "Humen", 'player-2': "Humen"})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.app.post('/start-game-connect4',\
                                    json={'player-1': "Humen", 'player-2': "Random Agent"})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.app.post('/start-game-connect4',\
                                    json={'player-1': "Random Agent", 'player-2': "Humen"})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        
        
    def test_get_state(self):
        self.app.post('/start-game-connect4',\
                                    json={'player-1': "Humen", 'player-2': "Humen"})
        response = self.app.get('/get-state-connect4')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertIsInstance(data_dict["state"]['board'], list)
        self.assertIsNotNone(data_dict.get("moves"))
        self.assertIsInstance(data_dict["moves"], list)
        
        
    def test_apply_move(self):
        # check that move from Humen side gets applied
        self.app.post('/start-game-connect4',\
                                    json={'player-1': "Humen", 'player-2': "Humen"})
        response = self.app.post('/apply-move', json={"column": 1, "player-id": 1, "is-bot": False})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        response = self.app.get('/get-state-connect4')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertEqual(data_dict["state"]["board"][-1][0], 1.0)
        
        # check that move from bots gets applied
        self.app.post('/start-game-connect4',\
                                    json={'player-1': "Random Agent", 'player-2': "Humen"})
        response = self.app.post('/apply-move', json={"column": 1, "player-id": 1, "is-bot": True})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        response = self.app.get('/get-state-connect4')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))

if __name__ == '__main__':
    unittest.main()