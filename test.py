from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homePage(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highScore'))
            self.assertIsNone(session.get('numPlays'))

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R", "O", "K", "R", "T"],
                                ["C", "C", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"]]
        response = self.client.get('/answer?word=rock')
        self.assertEqual(response.json['response'], 'ok')

    def test_not_on_board(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R", "O", "K", "R", "T"],
                                ["C", "C", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"]]
        response = self.client.get('/answer?word=kitten')
        self.assertEqual(response.json['response'], 'not-on-board')

    def test_invalid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R", "O", "K", "R", "T"],
                                ["C", "C", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"]]
        response = self.client.get('/answer?word=TK')
        self.assertEqual(response.json['response'], 'not-word')






            


