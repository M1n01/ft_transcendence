from django.db import models
from accounts.models import FtUser
from django.utils.translation import gettext_lazy as _
from .score_keeper.eth import (
    save_match_to_blockchain,
    get_matches_from_blockchain,
    delete_match_from_blockchain,
)


class Tournament(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name=_("トーナメント名"), max_length=16)
    organizer = models.ForeignKey(
        FtUser, on_delete=models.CASCADE, verbose_name=_("主催者")
    )
    start_at = models.DateTimeField(verbose_name=_("開始時間"))
    is_only_friend = models.BooleanField("フレンドのみ")
    current_players = models.IntegerField(verbose_name=_("最大参加人数"))

    def save(self, *args, **kwargs):
        if self.current_players < 4 or self.current_players > 32:
            raise ValueError("current_players must be between 4 and 32")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id={self.id}: {self.start_at} ({self.current_players} players)"


class TournamentParticipant(models.Model):
    id = models.BigAutoField(primary_key=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    participant = models.ForeignKey(FtUser, on_delete=models.CASCADE)
    is_accept = models.BooleanField()


"""
シード(正確には不戦勝)の場合はplayer2がnull
試合不成立の場合はplayer1,2のスコアが共にblank
"""

# from accounts.models import FtUser
# from django.utils.translation import gettext_lazy as _
from tournament.models import Tournament


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
        return matches[0] if matches else None

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
