from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.score_keeper_serializers import (
    MatchRequestSerializer,
    MatchResponseSerializer,
)
import json
import os
from django.conf import settings
from web3 import Web3
import datetime

# from web3.gas_strategies.time_based import medium_gas_price_strategy


def get_hardhat_compiled_contract():
    contract_path = os.path.join(
        settings.BLOCKCHAIN_DIR,
        "artifacts",
        "contracts",
        "PongScoreKeeper.sol",
        "PongScoreKeeper.json",
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
w3 = Web3(Web3.HTTPProvider(settings.PROVIDER_URL))
account = w3.eth.account.from_key(settings.PRIVATE_KEY)
contract_interface = get_hardhat_compiled_contract()
address = deploy_contract(contract_interface)
match_contract = w3.eth.contract(address=address, abi=contract_interface["abi"])


class SaveMatchScoreView(APIView):
    http_method_names = ["get", "post", "delete"]

    # TODO: クエリでのページネーション実装
    def get(self, request):
        match_id = request.query_params.get("match_id")
        user_id = request.query_params.get("user_id")
        if match_id:
            try:
                match = match_contract.functions.getMatch(int(match_id)).call()
                match_data = {
                    "id": match[0],
                    "created_at": datetime.datetime.fromtimestamp(match[1]),
                    "player1": match[3],
                    "player1_score": match[4],
                    "player2": match[5],
                    "player2_score": match[6],
                }
                serializer = MatchResponseSerializer(match_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving match", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif user_id:
            try:
                matches, match_length = match_contract.functions.getMatchesByUserId(
                    int(user_id),
                    True,  # DELETEした試合も含める場合はFalse
                    0,  # pagination page
                    100,  # pagination limit
                ).call()
                matches_data = [
                    {
                        "id": match[0],
                        "created_at": datetime.datetime.fromtimestamp(match[1]),
                        "player1": match[3],
                        "player1_score": match[4],
                        "player2": match[5],
                        "player2_score": match[6],
                    }
                    for match in matches
                ]
                serializer = MatchResponseSerializer(matches_data, many=True)
                return Response(
                    {"data": serializer.data, "match_length": match_length},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"message": "Error retrieving matches", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            try:
                matches, match_length = match_contract.functions.getAllMatches(
                    True,  # isActive
                    0,  # pagination page
                    100,  # pagination limit
                ).call()
                matches_data = [
                    {
                        "id": match[0],
                        "created_at": datetime.datetime.fromtimestamp(match[1]),
                        "player1": match[3],
                        "player1_score": match[4],
                        "player2": match[5],
                        "player2_score": match[6],
                    }
                    for match in matches
                ]
                serializer = MatchResponseSerializer(matches_data, many=True)
                return Response(
                    {"data": serializer.data, "match_length": match_length},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {"message": "Error retrieving match", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def post(self, request):
        serializer = MatchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = match_contract.functions.createMatch(
                serializer.validated_data["player1"],
                serializer.validated_data["player1_score"],
                serializer.validated_data["player2"],
                serializer.validated_data["player2_score"],
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
            logs = match_contract.events.MatchCreated().process_receipt(receipt)
            match_id = logs[0]["args"]["matchId"]
            created_at = logs[0]["args"]["createdAt"]

            return Response(
                {
                    "status": "match created",
                    "tx_hash": tx_hash.hex(),
                    "id": match_id,
                    "created_at": datetime.datetime.fromtimestamp(created_at),
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        match_id = request.query_params.get("match_id")
        if not match_id:
            return Response(
                {"error": "match_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transaction = match_contract.functions.toggleMatchStatus(
                int(match_id)
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

            logs = match_contract.events.MatchStatusChanged().process_receipt(receipt)
            is_active = logs[0]["args"]["isActive"]
            return Response(
                {
                    "status": "match deleted",
                    "tx_hash": tx_hash.hex(),
                    "is_active": is_active,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
