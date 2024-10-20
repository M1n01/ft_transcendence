from django.test import TestCase
from unittest.mock import patch
from .models import Match
import uuid


class MatchTestCase(TestCase):
    def setUp(self):
        self.match_id = uuid.uuid4()
        self.tournament_id = uuid.uuid4()
        self.player1_id = uuid.uuid4()
        self.player2_id = uuid.uuid4()

    @patch("pong.models.save_match_to_blockchain")
    def test_save_match(self, mock_save):

        mock_save.return_value = ("tx_hash_1", "2023-01-01 00:00:00")

        tx_hash, created_at = Match.save(
            match_id=self.match_id,
            tournament_id=self.tournament_id,
            round=1,
            player1_id=self.player1_id,
            player2_id=self.player2_id,
            player1_score=11,
            player2_score=8,
        )

        self.assertEqual(tx_hash, "tx_hash_1")
        self.assertEqual(created_at, "2023-01-01 00:00:00")
        mock_save.assert_called_once_with(
            self.match_id.bytes,
            self.tournament_id.bytes,
            self.player1_id.bytes,
            11,
            self.player2_id.bytes,
            8,
            1,
        )

    @patch("pong.models.get_matches_from_blockchain")
    def test_get_match_existing(self, mock_get):

        mock_get.return_value = [
            {
                "match_id": self.match_id,
                "tournament_id": self.tournament_id,
                "player1": self.player1_id,
                "player1_score": 11,
                "player2": self.player2_id,
                "player2_score": 8,
                "round": 1,
                "is_active": True,
            }
        ]
        match = Match.get_match(self.match_id)

        self.assertIsNotNone(match)
        self.assertEqual(match["match_id"], self.match_id)
        self.assertEqual(match["tournament_id"], self.tournament_id)
        self.assertEqual(match["player1"], self.player1_id)
        self.assertEqual(match["player2"], self.player2_id)
        self.assertEqual(match["player1_score"], 11)
        self.assertEqual(match["player2_score"], 8)
        self.assertEqual(match["round"], 1)
        self.assertTrue(match["is_active"])
        mock_get.assert_called_once_with(match_id=self.match_id)

    @patch("pong.models.get_matches_from_blockchain")
    def test_get_match_non_existing(self, mock_get):
        non_existing_match_id = uuid.uuid4()
        mock_get.return_value = []

        match = Match.get_match(non_existing_match_id)

        # matchが存在しない場合、要素なし
        self.assertEqual(match, [])
        mock_get.assert_called_once_with(match_id=non_existing_match_id)

    @patch("pong.models.get_matches_from_blockchain")
    def test_get_matches(self, mock_get):
        match_id2 = uuid.uuid4()

        mock_get.return_value = [
            {"match_id": self.match_id, "data": "data_1"},
            {"match_id": match_id2, "data": "data_2"},
        ]

        matches = Match.get_matches(
            tournament_id="tournament_1", user_id="user_1", round=1
        )

        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0]["match_id"], self.match_id)
        self.assertEqual(matches[1]["match_id"], match_id2)
        mock_get.assert_called_once_with(
            tournament_id="tournament_1", user_id="user_1", round=1
        )

    @patch("pong.models.delete_match_from_blockchain")
    def test_delete_match_success(self, mock_delete):
        mock_delete.return_value = "tx_hash_1"

        result = Match.delete_match(self.match_id)

        self.assertTrue(result)
        mock_delete.assert_called_once_with(self.match_id)

    @patch("pong.models.delete_match_from_blockchain")
    def test_delete_match_failure(self, mock_delete):
        non_existing_match_id = uuid.uuid4()
        mock_delete.return_value = None

        result = Match.delete_match(non_existing_match_id)

        self.assertFalse(result)
        mock_delete.assert_called_once_with(non_existing_match_id)
