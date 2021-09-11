from unittest import TestCase

from app import app, games
from random import sample
from flask import jsonify

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertNotEqual(response.status_code, 404) #could be a 304 (cache). Use status code for Failures
            self.assertIn('<title>Boggle</title>', html)
            self.assertIn('<ul id="words"', html) #may add more things so don't add close tag

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            parsed_data = response.get_json()

            self.assertIsNotNone(parsed_data)
            self.assertTrue(parsed_data["gameId"])
            self.assertTrue(parsed_data["board"])
            self.assertIsInstance(parsed_data["gameId"], str)
            self.assertIsInstance(parsed_data["board"], list)
            self.assertIsInstance(parsed_data["board"][0], list)
            self.assertTrue(games)
        
    def test_api_score_word(self):
        """Test api_score_word function for word validity, and return json {"result": <status>} """

        with self.client as client:
            response = client.post("/api/new-game")
            parsed_data = response.get_json()

            #fake game board:
            game_id = parsed_data["gameId"]
            game = games[game_id]
            game.board = [['J', 'O', 'V', 'C', 'O'],      
                        ['N', 'O', 'C', 'V', 'F'],
                        ['R', 'O', 'J', 'E', 'I'],
                        ['K', 'N', 'P', 'W', 'K'],
                        ['J', 'E', 'A', 'I', 'E']]
            

            WORD_ON_BOARD = "NOPE"
            NOT_ON_BOARD = "COFFEE"                       
            NOT_A_WORD = "SLEKFJ"

            BASE_ROUTE = "/api/score-word"
            
            #testing for new existing word
            resp = client.post(BASE_ROUTE, 
                json={"game_id": game_id, "word": WORD_ON_BOARD})  
            self.assertEqual(resp.get_json(), {"result": "ok"})


            #testing for valid word but not on board
            resp = client.post(BASE_ROUTE, 
                json={"game_id": game_id, "word": NOT_ON_BOARD})  
            self.assertEqual(resp.get_json(), {"result": "not-on-board"})

            #testing for invalid word
            resp = client.post(BASE_ROUTE, 
                json={"game_id": game_id, "word": NOT_A_WORD}) 
            self.assertEqual(resp.get_json(), {"result": "not-word"})
