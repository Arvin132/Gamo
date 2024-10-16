import unittest
from backend import app
import json

class GamoFlaskTest_Backend(unittest.TestCase):

    # Setup method to configure the test environment
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # When using test_client, the port is irrelevant because requests are simulated internally

    def test_running(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data.decode() == None)
        
    def test_connect4_agents_list(self):
        response = self.app.get('/get-agents-list')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data_dict["agents"])
        
    def test_connect4_start_connect4(self):
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
        
        
        
    def test_get_state_connect4(self):
        self.app.post('/start-game-connect4',\
                                    json={'player-1': "Humen", 'player-2': "Humen"})
        response = self.app.get('/get-state-connect4')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertIsInstance(data_dict["state"]['board'], list)
        self.assertIsNotNone(data_dict.get("move"))
        self.assertIsNotNone(data_dict["move"].get("column"))
        
        
    def test_apply_move_connect(self):
        self.app.post('/start-game-connect4',\
                                    json={'player-1': "Humen", 'player-2': "Humen"})
        response = self.app.post('/apply-move', json={"column": 1, "player-id": 1, "is-bot": False})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.app.get('/get-state-connect4')
        data_dict = json.loads(response.data.decode('utf-8'))
        print(data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertEqual(data_dict["state"]["board"][-1][0], 1.0)

        self.app.post('/start-game-connect4',\
                                    json={'player-1': "Random Agent", 'player-2': "Humen"})
        response = self.app.post('/apply-move', json={"column": 1, "player-id": 1, "is-bot": True})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.app.get('/get-state-connect4')
        data_dict = json.loads(response.data.decode('utf-8'))
        print(data_dict)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))

if __name__ == '__main__':
    unittest.main()