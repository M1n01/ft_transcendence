from django.test import TestCase
from unittest.mock import patch
from .models import Match


class MatchTestCase(TestCase):
    @patch("pong.models.save_match_to_blockchain")
    def test_save_match(self, mock_save):
        mock_save.return_value = ("match_id_1", "tx_hash_1", "2023-01-01 00:00:00")

        match_id, tx_hash, created_at = Match.save(
            tournament_id="tournament_1",
            round=1,
            player1_id="player_1",
            player2_id="player_2",
            player1_score=11,
            player2_score=8,
        )

        self.assertEqual(match_id, "match_id_1")
        self.assertEqual(tx_hash, "tx_hash_1")
        self.assertEqual(created_at, "2023-01-01 00:00:00")
        mock_save.assert_called_once_with(
            "tournament_1", "player_1", 11, "player_2", 8, 1
        )

    @patch("pong.models.get_matches_from_blockchain")
    def test_get_match_existing(self, mock_get):
        mock_get.return_value = [{"match_id": "match_1", "data": "some_data"}]

        match = Match.get_match("match_1")

        self.assertIsNotNone(match)
        self.assertEqual(match["match_id"], "match_1")
        mock_get.assert_called_once_with(match_id="match_1")

    @patch("pong.models.get_matches_from_blockchain")
    def test_get_match_non_existing(self, mock_get):
        mock_get.return_value = []

        match = Match.get_match("non_existing_match")

        self.assertIsNone(match)
        mock_get.assert_called_once_with(match_id="non_existing_match")

    @patch("pong.models.get_matches_from_blockchain")
    def test_get_matches(self, mock_get):
        mock_get.return_value = [
            {"match_id": "match_1", "data": "data_1"},
            {"match_id": "match_2", "data": "data_2"},
        ]

        matches = Match.get_matches(
            tournament_id="tournament_1", user_id="user_1", round=1
        )

        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0]["match_id"], "match_1")
        self.assertEqual(matches[1]["match_id"], "match_2")
        mock_get.assert_called_once_with(
            tournament_id="tournament_1", user_id="user_1", round=1
        )

    @patch("pong.models.delete_match_from_blockchain")
    def test_delete_match_success(self, mock_delete):
        mock_delete.return_value = "tx_hash_1"

        result = Match.delete_match("match_1")

        self.assertTrue(result)
        mock_delete.assert_called_once_with("match_1")

    @patch("pong.models.delete_match_from_blockchain")
    def test_delete_match_failure(self, mock_delete):
        mock_delete.return_value = None

        result = Match.delete_match("non_existing_match")

        self.assertFalse(result)
        mock_delete.assert_called_once_with("non_existing_match")
