from web3 import Web3
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
    match_id, tournament, player1, player1_score, player2, player2_score, round
):

    w3 = get_contract()
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_hardhat_compiled_contract()["abi"],
    )

    account = w3.eth.account.from_key(settings.PRIVATE_ACCOUNT_KEY)

    try:
        match_id_bytes = match_id.bytes
        tournament_bytes = tournament.bytes
        player1_bytes = player1.bytes
        player2_bytes = player2.bytes
        print(
            "variants", match_id_bytes, tournament_bytes, player1_bytes, player2_bytes
        )
        transaction = contract.functions.createMatch(
            match_id_bytes,
            tournament_bytes,
            player1_bytes,
            player1_score,
            player2_bytes,
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

        signed_txn = w3.eth.account.sign_transaction(
            transaction, settings.PRIVATE_ACCOUNT_KEY
        )

        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)


        # イベントをキャッチしてタイムスタンプを取得
        print("Waiting for transaction receipt...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction receipt received: {receipt}")

        if receipt.status == 0:
            print("Transaction failed")
            raise Exception("Transaction failed")

        print("Processing logs...")
        logs = contract.events.MatchCreated().process_receipt(receipt)
        print(f"Logs processed: {logs}")

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
        utc_created_at = datetime.fromtimestamp(match[1], tz=timezone.utc)
        jst_created_at = utc_created_at.astimezone(timezone(timedelta(hours=9)))
        return {
            "match_id": uuid.UUID(bytes=match[0]),
            "tournament_id": uuid.UUID(bytes=match[2]),
            "player1": uuid.UUID(bytes=match[3]),
            "player2": uuid.UUID(bytes=match[4]),
            "created_at": jst_created_at,
            "player1_score": match[5],
            "player2_score": match[6],
            "round": match[7],
            "is_active": match[8],
        }

    if match_id is not None:
        match_id_bytes = match_id.bytes
        match = contract.functions.getMatch(match_id_bytes, only_active).call()
        matches = match_to_dict(match)
    else:
        all_matches = contract.functions.getAllMatches(only_active).call()
        if user_id:
            user_id_bytes = user_id.bytes
            # ユーザーIDを指定した場合、player1かplayer2にユーザーIDが含まれるものを抽出
            matches = [
                match
                for match in all_matches
                if match[3] == user_id_bytes or match[4] == user_id_bytes
            ]
        elif tournament_id:
            tournament_id_bytes = tournament_id.bytes
            matches = [
                match for match in all_matches if match[2] == tournament_id_bytes
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
        match_id_bytes = match_id.bytes
        transaction = contract.functions.deleteMatch(match_id_bytes).build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = w3.eth.account.sign_transaction(
            transaction, settings.PRIVATE_ACCOUNT_KEY
        )
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return tx_hash

    except Exception as e:
        print(f"Error deleting match from blockchain: {e}")
        return None
