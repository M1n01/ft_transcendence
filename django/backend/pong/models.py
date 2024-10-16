from django.db import models
from accounts.models import FtUser
from .score_keeper.eth import (
    save_match_to_blockchain,
    get_matches_from_blockchain,
    delete_match_from_blockchain,
)
from tournament.models import Tournament

import uuid


"""
シード(正確には不戦勝)の場合はplayer2がnull
試合不成立の場合はplayer1,2のスコアが共にblank
"""


class Match:
    @classmethod
    def save(
        cls,
        tournament_id,
        round,
        player1_id,
        player2_id,
        player1_score,
        player2_score,
    ):
        # ブロックチェーンにマッチ情報を保存
        match_id, tx_hash, created_at = save_match_to_blockchain(
            tournament_id,
            player1_id,
            player1_score,
            player2_id,
            player2_score,
            round,
        )
        return match_id, tx_hash, created_at

    @classmethod
    def get_match(cls, match_id):
        # ブロックチェーンから単一のマッチ情報を取得
        matches = get_matches_from_blockchain(match_id=match_id)
        return matches

    @classmethod
    def get_matches(cls, tournament_id=None, user_id=None, round=None):
        # ブロックチェーンから複数のマッチ情報を取得
        # 全てNoneの場合は全マッチを取得
        matches = get_matches_from_blockchain(
            tournament_id=tournament_id,
            user_id=user_id,
            round=round,
        )
        return matches

    @classmethod
    def delete_match(cls, match_id):
        # ブロックチェーンからマッチ情報を削除
        tx_hash = delete_match_from_blockchain(match_id)

        if tx_hash:
            return True
        else:
            return False


class MatchTmp(models.Model):
    """
    Matchと内容はほぼ同じ
    BlockChainではなく、DBに保持する一時データ
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tournament_id = models.ForeignKey(Tournament, on_delete=models.PROTECT, null=True)
    round = models.SmallIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    player1 = models.ForeignKey(
        FtUser, on_delete=models.PROTECT, null=True, related_name="player1"
    )
    player2 = models.ForeignKey(
        FtUser, on_delete=models.PROTECT, null=True, related_name="player2"
    )
    player1_score = models.SmallIntegerField(default=0)
    player2_score = models.SmallIntegerField(default=0)

    def __str__(self):
        return (
            f"id={self.id}:{self.round=} {self.player1} vs {self.player2} "
            + f"(player1_score={self.player1_score}, player2_score={self.player2_score})"
        )
