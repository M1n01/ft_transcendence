from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, SmartContract
from .serializers import GameRequestSerializer, GameResponseSerializer
import json
import os
from django.conf import settings
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version

# from web3.gas_strategies.time_based import medium_gas_price_strategy


class SaveGameScoreView(APIView):
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider("http://contracts:8545"))
        # self.web3.eth.set_gas_price_strategy(medium_gas_price_strategy)  # ガス価格を設定
        self.account = self.web3.eth.accounts[0]  # ノードのaccount[0]を使用
        self.setup_contract()

    def setup_contract(self):
        try:
            contract = SmartContract.objects.get(name="ScoreKeeper")
            self.game_contract = self.web3.eth.contract(
                address=contract.address, abi=contract.abi
            )
        except SmartContract.DoesNotExist:
            compiled_sol = self.compile_source_file()
            contract_id, contract_interface = compiled_sol.popitem()
            address = self.deploy_contract(contract_interface)
            SmartContract.objects.create(
                name="ScoreKeeper", address=address, abi=contract_interface["abi"]
            )
            self.game_contract = self.web3.eth.contract(
                address=address, abi=contract_interface["abi"]
            )

    def compile_source_file(self):
        install_solc(version="0.8.24")
        contract_path = os.path.join(
            settings.BLOCKCHAIN_DIR, "contracts", "ScoreKeeper.sol"
        )
        with open(contract_path, "r") as file:
            contract_source_file = file.read()

        compiled_sol = compile_source(
            contract_source_file, output_values=["abi", "bin"]
        )
        return compiled_sol

    def deploy_contract(self, contract_interface):
        contract = self.web3.eth.contract(
            abi=contract_interface["abi"], bytecode=contract_interface["bin"]
        )

        contract_owner = [self.account.address]

        transaction = contract.constructor(contract_owner).build_transaction(
            {
                "from": self.account,
                "nonce": self.web3.eth.get_transaction_count(self.account),
            }
        )
        signed_txn = self.web3.eth.account.sign_transaction(transaction)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def get_contract(self):
        return self.game_contract

    def get(self, request):
        game_id = request.query_params.get("game_id")
        user_id = request.query_params.get("user_id")
        if game_id:
            try:
                game = self.game_contract.functions.getGame(int(game_id)).call()
                serializer = GameResponseSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving game", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        elif user_id:
            try:
                games = self.game_contract.functions.getGamesByUser(int(user_id)).call()
                serializer = GameResponseSerializer(games, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"message": "Error retrieving games", "error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            try:
                games = self.game_contract.functions.getAllGame().call()
                serializer = GameResponseSerializer(games, many=True)
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
            transaction = self.game_contract.functions.createGame(
                serializer.validated_data["winner"],
                serializer.validated_data["winner_score"],
                serializer.validated_data["loser"],
                serializer.validated_data["loser_score"],
            ).build_transaction(
                {
                    "from": os.getenv("CONTRACT_OWNER_ADDRESS"),
                    "nonce": self.web3.eth.get_transaction_count(
                        os.getenv("CONTRACT_OWNER_ADDRESS")
                    ),
                }
            )

            signed_txn = self.web3.eth.account.sign_transaction(
                transaction, private_key=os.getenv("CONTRACT_OWNER_PRIVATE_KEY")
            )
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

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
