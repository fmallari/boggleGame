from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
    # TODO -- write tests for every view function / feature!

        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_homepage(self):
        """Ensure information is in session and HTML is displayed"""

        with self.client:
            response = self.cliet.get('/')
            self.assertin('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
    
    def test_valid_word(self):
        """Test if word is valid by modifying the board in session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"]]
        response = self.client.get('/check-word?word=dog')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in dictionary"""

        self.client.get('/')
        response = self.client.gt('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on board"""

        self.client.get('/')
        response = self.client.get(
            '/word=vmiaoeurfjjaskdnfjadnfasdf')
        self.assertEqual(response.json['result'], 'not-word')
          