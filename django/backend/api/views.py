from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Score
from .models import Comment
from .serializers import ScoreSerializer
from web3 import Web3
import json
import os
from django.conf import settings

# ローカルのイーサリアム環境に接続
web3 = Web3(Web3.HTTPProvider("http://contracts:8545"))

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
        match_id = request.query_params.get("match_id")  # クエリを使用
        if match_id:
            try:
                # 試合データの取得
                match = match_contract.functions.getMatch(int(match_id)).call()

                # データの構造を変数に分ける
                match_id = match[0]
                player_id, player_score = match[1]
                opponent_id, opponent_score = match[2]

                # レスポンスの作成
                response_data = {
                    "message": "Match retrieved",
                    "match_id": match_id,
                    "player": {
                        "id": player_id,
                        "score": player_score,
                    },
                    "opponent": {
                        "id": opponent_id,
                        "score": opponent_score,
                    },
                }

                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving match", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            try:
                match_count = match_contract.functions.getMatchCount().call()
                return Response(
                    {"message": "Match count retrieved", "match_count": match_count},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"message": "Error retrieving match count", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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

            try:
                txn = match_contract.functions.addMatch(
                    match_id, player_id, player_score, opponent_id, opponent_score
                ).build_transaction(
                    {
                        "from": web3.eth.accounts[0],
                        "nonce": web3.eth.get_transaction_count(web3.eth.accounts[0]),
                    }
                )

                signed_txn = web3.eth.account.sign_transaction(
                    txn, private_key=os.getenv("CONTRACT_OWNER_PRIVATE_KEY")
                )
                tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                return Response(
                    {
                        "status": "Match created",
                        "tx_hash": tx_hash.hex(),
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
