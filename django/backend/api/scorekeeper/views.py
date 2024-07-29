from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Match
from .serializers import MatchSerializer
from web3 import Web3
import json
import os
from django.conf import settings

# infuraのURL
infura_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(infura_url))

# hardhatコントラクトインスタンスの取得
project_root = "/workspace"
json_path = os.path.join(
    project_root,
    "solidity",
    "artifacts",
    "contracts",
    "ScoreKeeper.sol",
    "ScoreKeeper.json",
)

with open(json_path) as f:
    scorekeeper_json = json.load(f)
contract_abi = scorekeeper_json["abi"]
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

match_contract = web3.eth.contract(address=contract_address, abi=contract_abi)


class MatchAPIViewSet(APIView):
    def get(self, request, format=None):
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MatchSerializer(data=request.data)
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
