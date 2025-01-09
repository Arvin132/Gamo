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
        response = self.app.get('/connect4/agents')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data_dict.get("agents")) # check that agents exist
        
    def test_start_game(self):
        # check for all the different possible assignments
        response = self.app.post('/connect4/start',\
                                    json={'player-1': "Human", 'player-2': "Human"})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.app.post('/connect4/start',\
                                    json={'player-1': "Human", 'player-2': "Random Agent"})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        response = self.app.post('/connect4/start',\
                                    json={'player-1': "Random Agent", 'player-2': "Human"})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        
        
        
    def test_get_state(self):
        self.app.post('/connect4/start',\
                                    json={'player-1': "Human", 'player-2': "Human"})
        response = self.app.get('/connect4/state')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertIsInstance(data_dict["state"]['board'], list)
        self.assertIsNotNone(data_dict.get("moves"))
        self.assertIsInstance(data_dict["moves"], list)
        
        
    def test_apply_move(self):
        # check that move from Human side gets applied
        self.app.post('/connect4/start',\
                                    json={'player-1': "Human", 'player-2': "Human"})
        response = self.app.post('/connect4/apply-move', json={"column": 1, "player-id": 1, "is-bot": False})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        response = self.app.get('/connect4/state')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        self.assertEqual(data_dict["state"]["board"][-1][0], 1.0)
        
        # check that move from bots gets applied
        self.app.post('/connect4/start',\
                                    json={'player-1': "Random Agent", 'player-2': "Human"})
        response = self.app.post('/connect4/apply-move', json={"column": 1, "player-id": 1, "is-bot": True})
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))
        response = self.app.get('/connect4/state')
        data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_dict["message"].startswith("200"))


class GamoFlaskTest_Backend_User(unittest.TestCase):
    # Setup method to configure the test environment
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_user_few(self):
        response = self.app.get('/user/get-few')
        data_dict = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data_dict.get("users"))
        self.assertTrue(len(data_dict.get("users")) != 0)

    def test_user_get(self):
        response = self.app.get('/user/get', json={'id' : 1}) 
        data_dict = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data_dict.get("id"))
        self.assertEqual(data_dict["id"], 1)
        self.assertIsNotNone(data_dict.get("username"))
if __name__ == '__main__':
    unittest.main()