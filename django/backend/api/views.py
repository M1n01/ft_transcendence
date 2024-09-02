from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game
from .serializers import GameRequestSerializer, GameResponseSerializer
import json
import os
from django.conf import settings
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
import datetime

# from web3.gas_strategies.time_based import medium_gas_price_strategy


def get_hardhat_compiled_contract():
    contract_path = os.path.join(
        settings.BLOCKCHAIN_DIR,
        "artifacts",
        "contracts",
        "ScoreKeeper.sol",
        "ScoreKeeper.json",
    )
    with open(contract_path, "r") as file:
        contract_json = json.load(file)
    return {"abi": contract_json["abi"], "bin": contract_json["bytecode"]}


def deploy_contract(contract_interface):
    contract = w3.eth.contract(
        abi=contract_interface["abi"], bytecode=contract_interface["bin"]
    )

    address = account.address

    transaction = contract.constructor(address).build_transaction(
        {
            "from": address,
            "nonce": w3.eth.get_transaction_count(address),
        }
    )
    signed_txn = w3.eth.account.sign_transaction(transaction, settings.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress


# ブロックチェーンの接続
w3 = Web3(Web3.HTTPProvider("http://eth:8545"))
account = w3.eth.account.from_key(settings.PRIVATE_KEY)
contract_interface = get_hardhat_compiled_contract()
address = deploy_contract(contract_interface)
game_contract = w3.eth.contract(address=address, abi=contract_interface["abi"])


class SaveGameScoreView(APIView):
    def get(self, request):
        game_id = request.query_params.get("game_id")
        user_id = request.query_params.get("user_id")
        if game_id:
            try:
                game = game_contract.functions.getGame(int(game_id)).call()
                game_data = {
                    "id": game[0],
                    "created_at": datetime.datetime.fromtimestamp(game[1]),
                    "winner": game[2],
                    "winner_score": game[3],
                    "loser": game[4],
                    "loser_score": game[5],
                }
                serializer = GameResponseSerializer(game_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving game", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif user_id:
            try:
                games = game_contract.functions.findGameByUserId(int(user_id)).call()
                games_data = [
                    {
                        "id": game[0],
                        "created_at": datetime.datetime.fromtimestamp(game[1]),
                        "winner": game[2],
                        "winner_score": game[3],
                        "loser": game[4],
                        "loser_score": game[5],
                    }
                    for game in games
                ]
                serializer = GameResponseSerializer(games_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving games", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            try:
                games = game_contract.functions.getAllGame().call()
                games_data = [
                    {
                        "id": game[0],
                        "created_at": datetime.datetime.fromtimestamp(game[1]),
                        "winner": game[2],
                        "winner_score": game[3],
                        "loser": game[4],
                        "loser_score": game[5],
                    }
                    for game in games
                ]
                serializer = GameResponseSerializer(games_data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving game", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def post(self, request):
        serializer = GameRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = game_contract.functions.createGame(
                serializer.validated_data["winner"],
                serializer.validated_data["winner_score"],
                serializer.validated_data["loser"],
                serializer.validated_data["loser_score"],
            ).build_transaction(
                {
                    "from": account.address,
                    "nonce": w3.eth.get_transaction_count(account.address),
                }
            )

            signed_txn = w3.eth.account.sign_transaction(
                transaction, settings.PRIVATE_KEY
            )
            tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            # イベントをキャッチしてタイムスタンプを取得
            logs = game_contract.events.GameCreated().process_receipt(receipt)
            game_id = logs[0]["args"]["matchId"]
            created_at = logs[0]["args"]["createdAt"]

            return Response(
                {
                    "status": "game created",
                    "tx_hash": tx_hash.hex(),
                    "data": serializer.data,
                    "id": game_id,
                    "created_at": created_at,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
