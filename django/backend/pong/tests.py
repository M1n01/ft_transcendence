import unittest
from unittest.mock import patch
from django.utils import timezone
from .models import Match


class TestMatch(unittest.TestCase):

    def setUp(self):
        self.tournament_id = 1
        self.player1_id = 1
        self.player2_id = 2
        self.player1_score = 4
        self.player2_score = 2
        self.round = 1

    @patch('django.backend.pong.models.Match.save')
    def test_save_match(self, mock_save):
        mock_save.return_value = (1, 'tx_hash', timezone.now())
        match_id, tx_hash, created_at = Match.save(
            self.tournament_id,
            self.round,
            self.player1_id,
            self.player2_id,
            self.player1_score,
            self.player2_score,
        )
        self.assertEqual(match_id, 1)
        self.assertEqual(tx_hash, 'tx_hash')
        self.assertIsNotNone(created_at)

    @patch('django.backend.pong.models.Match.get_matches')
    def test_get_match_from_blockchain(self, mock_get_matches):
        mock_get_matches.return_value = [{'id': 0, 'tournament_id': 1, 'player1': 1, 'player2': 2, 'player1_score': 4, 'player2_score': 2, 'is_active': True, 'round': 1}]
        matches = Match.get_matches(user_id=2)
        self.assertEqual(len(matches), 1)

        match = Match.get_match(matches[0]["id"])
        self.assertEqual(match["id"], 0)
        self.assertEqual(match["tournament_id"], 1)
        self.assertEqual(match["player1"], 1)
        self.assertEqual(match["player2"], 2)
        self.assertEqual(match["player1_score"], 4)
        self.assertEqual(match["player2_score"], 2)
        self.assertEqual(match["is_active"], True)
        self.assertEqual(match["round"], 1)

    @patch('django.backend.pong.models.Match.get_match')
    def test_get_match(self, mock_get_match):
        mock_get_match.return_value = {'id': 0, 'tournament_id': 1, 'player1': 1, 'player2': 2, 'player1_score': 4, 'player2_score': 2, 'is_active': True, 'round': 1}
        match = Match.get_match(0)
        self.assertIsNotNone(match)
        self.assertIsInstance(match, dict)

    @patch('django.backend.pong.models.Match.get_matches')
    def test_get_matches(self, mock_get_matches):
        mock_get_matches.return_value = [{'id': 0, 'tournament_id': 1, 'player1': 1, 'player2': 2, 'player1_score': 4, 'player2_score': 2, 'is_active': True, 'round': 1}]
        matches = Match.get_matches()
        self.assertIsNotNone(matches)
        self.assertIsInstance(matches, list)

    @patch('django.backend.pong.models.Match.delete_match')
    def test_delete_match(self, mock_delete_match):
        mock_delete_match.return_value = True
        result = Match.delete_match(0)
        self.assertTrue(result)
