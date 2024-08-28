from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game
from .serializers import GameRequestSerializer, GameResponseSerializer
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

game_contract = web3.eth.contract(address=contract_address, abi=contract_abi)


class SaveGameScoreView(APIView):
    def get(self, request, format=None):
        game_id = request.query_params.get("match_id")  # クエリを使用
        if game_id:
            request_data = request.data.copy()
            request_data["match_id"] = game_id
            try:
                game = game_contract.functions.getGame(int(game_id)).call()
                serializer = GameResponseSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving game", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {"message": "No game_id provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, format=None):
        serializer = GameRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                txn = game_contract.functions.createGame(
                    serializer.validated_data["winner"],
                    serializer.validated_data["winner_score"],
                    serializer.validated_data["loser"],
                    serializer.validated_data["loser_score"],
                ).build_transaction(
                    {
                        "from": web3.eth.accounts[0],
                        "nonce": web3.eth.get_transaction_count(web3.eth.accounts[0]),
                    }
                )

                signed_txn = web3.eth.account.sign_transaction(
                    txn, private_key=os.getenv("CONTRACT_OWNER_PRIVATE_KEY")
                )
                tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                return Response(
                    {
                        "status": "game created",
                        "tx_hash": tx_hash.hex(),
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
