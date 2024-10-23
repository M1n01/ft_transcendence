from web3 import Web3, exceptions
from django.conf import settings
import os
import json
import uuid
from datetime import datetime, timezone, timedelta


def get_contract():
    return Web3(Web3.HTTPProvider(settings.PROVIDER_URL))


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


def get_contract_address():
    with open(os.path.join(settings.BLOCKCHAIN_DIR, "contract_address.txt")) as file:
        return file.read()


def save_match_to_blockchain(
    match_id, tournament_id, player1_id, player2_id, player1_score, player2_score, round
):

    w3 = get_contract()
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_hardhat_compiled_contract()["abi"],
    )

    account = w3.eth.account.from_key(settings.PRIVATE_ACCOUNT_KEY)

    try:
        match_id_int = match_id.int
        tournament_id_int = tournament_id.int
        player1_id_int = player1_id.int
        player2_id_int = player2_id.int

        try:
            transaction = contract.functions.createMatch(
                match_id_int,
                tournament_id_int,
                player1_id_int,
                player2_id_int,
                player1_score,
                player2_score,
                round,
            ).build_transaction(
                {
                    "from": account.address,
                    "nonce": w3.eth.get_transaction_count(account.address),
                    "gas": 300000,
                    "gasPrice": w3.eth.gas_price,
                }
            )
        except exceptions.SolidityError as e:
            print(f"Error building transaction: {e}")
            raise Exception("Error building transaction")

        signed_txn = w3.eth.account.sign_transaction(
            transaction, settings.PRIVATE_ACCOUNT_KEY
        )

        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # イベントをキャッチしてタイムスタンプを取得
        print("Waiting for transaction receipt...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 0:
            print("Transaction failed")
            raise Exception("Transaction failed")

        print("Processing logs...")
        logs = contract.events.MatchCreated().process_receipt(receipt)

        # logsが空の配列の場合のハンドリングを追加
        if not logs:
            print("No logs found in receipt")
            return tx_hash.hex(), None

        try:
            unix_created_at = logs[0]["args"]["createdAt"]
            utc_created_at = datetime.fromtimestamp(unix_created_at, tz=timezone.utc)
            jst_created_at = utc_created_at.astimezone(timezone(timedelta(hours=9)))
            return tx_hash.hex(), jst_created_at
        except (IndexError, KeyError) as e:
            print(f"Error processing logs: {e}")
            # トランザクションは成功しているのでhashは返す
            return tx_hash.hex(), None

    except Exception as e:
        print(f"Error saving match to blockchain: {e}")
        return None, None


def get_matches_from_blockchain(
    match_id=None, tournament_id=None, user_id=None, round=None, only_active=True
):
    w3 = get_contract()
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_hardhat_compiled_contract()["abi"],
    )

    def match_to_dict(match):
        utc_created_at = datetime.fromtimestamp(match[2], tz=timezone.utc)
        jst_created_at = utc_created_at.astimezone(timezone(timedelta(hours=9)))
        return {
            "match_id": uuid.UUID(int=match[0]),
            "tournament_id": uuid.UUID(int=match[1]),
            "player1_id": uuid.UUID(int=match[3]),
            "player2_id": uuid.UUID(int=match[4]),
            "created_at": jst_created_at,
            "player1_score": match[5],
            "player2_score": match[6],
            "round": match[7],
            "is_active": match[8],
        }

    if match_id is not None:
        match_id_int = match_id.int

        try:
            match = contract.functions.getMatch(match_id_int, only_active).call()
        except exceptions.SolidityError as e:
            print(f"Error getting match: {e}")
            raise Exception("Error getting match")

        matches = match_to_dict(match)
    else:
        try:
            all_matches = contract.functions.getAllMatches(only_active).call()
        except exceptions.SolidityError as e:
            print(f"Error getting all matches: {e}")
            raise Exception("Error getting all matches")

        if user_id:
            user_id_int = user_id.int
            # ユーザーIDを指定した場合、player1かplayer2にユーザーIDが含まれるものを抽出
            matches = [
                match
                for match in all_matches
                if match[3] == user_id_int or match[4] == user_id_int
            ]
        elif tournament_id:
            tournament_id_int = tournament_id.int
            matches = [
                match
                for match in all_matches
                if match[1] == tournament_id_int and (round is None or match[7] == round)
            ]
        else:
            matches = all_matches
        matches = [match_to_dict(match) for match in matches]
    return matches


def delete_match_from_blockchain(match_id):
    w3 = get_contract()
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_hardhat_compiled_contract()["abi"],
    )

    account = w3.eth.account.from_key(settings.PRIVATE_ACCOUNT_KEY)

    try:
        match_id_int = match_id.int
        try:
            transaction = contract.functions.deleteMatch(
                match_id_int
            ).build_transaction(
                {
                    "from": account.address,
                    "nonce": w3.eth.get_transaction_count(account.address),
                }
            )
        except exceptions.SolidityError as e:
            print(f"Error building transaction: {e}")
            raise Exception("Error building transaction")

        signed_txn = w3.eth.account.sign_transaction(
            transaction, settings.PRIVATE_ACCOUNT_KEY
        )
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return tx_hash

    except Exception as e:
        print(f"Error deleting match from blockchain: {e}")
        return None
