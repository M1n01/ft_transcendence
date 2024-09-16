import unittest
from unittest.mock import patch
from django.utils import timezone
from .models import Match


class TestMatch(unittest.TestCase):

    def setUp(self):
        tournament_id = 1
        player1_id = 1
        player2_id = 2
        player1_score = 4
        player2_score = 2
        round = 1
        match_id, tx_hash, created_at = Match.save(
            tournament_id,
            round,
            player1_id,
            player2_id,
            player1_score,
            player2_score,
        )
        print("match_id", match_id)
        print("tx_hash", tx_hash)
        print("created_at", created_at)

    def test_get_match_from_blockchain(self):
        matches = Match.get_matches(user_id=2)
        print(matches)
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

    # def test_get_match(self):
    #     match = Match.get_match()
    #     self.assertIsNotNone(match)
    #     self.assertIsInstance(match, Match)

    # def test_get_matches(self):
    #     matches = Match.get_matches()
    #     self.assertIsNotNone(matches)
    #     self.assertIsInstance(matches, list)
