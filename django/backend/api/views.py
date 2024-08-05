from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Score
from .serializers import ScoreSerializer
from web3 import Web3
import json
import os
from django.conf import settings

# ローカルのイーサリアム環境に接続
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# hardhatコントラクトインスタンスの取得
json_path = os.path.join(
    settings.BLOCKCHAIN_DIR,
    "artifacts",
    "contracts",
    "ScoreKeeper.sol",
    "ScoreKeeper.json",
)

with open(json_path) as f:
    scorekeeper_json = json.load(f)
contract_abi = scorekeeper_json["abi"]
contract_address = os.getenv("CONTRACT_OWNER_ADDRESS")

match_contract = web3.eth.contract(address=contract_address, abi=contract_abi)


class ScoreAPIView(APIView):
    def get(self, request, format=None):
        scores = Score.objects.all()
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            match_id = serializer.validated_data["match_id"]
            player = serializer.validated_data["player"]
            opponent = serializer.validated_data["opponent"]

            player_id = player["player_id"]
            player_score = player["score"]
            opponent_id = opponent["player_id"]
            opponent_score = opponent["score"]

            # トランザクションの送信
            tx_hash = match_contract.functions.createMatch(
                match_id, player_id, player_score, opponent_id, opponent_score
            ).transact({"from": web3.eth.accounts[0]})

            # トランザクションの確認
            receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            return Response(
                {"status": "Match created", "tx_hash": tx_hash.hex()},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
