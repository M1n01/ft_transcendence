from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Match
from .serializers import MatchSerializer
from web3 import Web3
import json


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Web3の設定
        infura_url = "http://127.0.0.1:8545"
        web3 = Web3(Web3.HTTPProvider(infura_url))

        print(web3.isConnected())

        # hardhatコントラクトインスタンスの取得
        with open("hardhat/artifacts/contracts/ScoreKeeper.sol/ScorKeeper.json") as f:
            scorekeeper_json = json.load(f)
        abi = scorekeeper_json["abi"]
        contract_address = scorekeeper_json["contractAddress"]
        contract = web3.eth.contract(address=contract_address, abi=abi)

        # トランザクションの作成
        tx = contract.functions.addMatch(
            serializer.data["match_id"],
            serializer.data["player"]["player_id"],
            serializer.data["player"]["score"],
            serializer.data["opponent"]["player_id"],
            serializer.data["opponent"]["score"],
        ).buildTransaction({"from": web3.eth.default_account})

        # トランザクションの署名と送信
        signed_tx = web3.eth.account.signTransaction(tx, private_key="0x")
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return Response(
            {"tx_hash": web3.toHex(tx_hash)},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
