from web3 import Web3
from django.conf import settings
import os
import json


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
    tournament, player1, player1_score, player2, player2_score, round
):

    w3 = get_contract()
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_hardhat_compiled_contract()["abi"],
    )

    account = w3.eth.account.from_key(settings.PRIVATE_KEY)

    try:
        transaction = contract.functions.createMatch(
            tournament,
            player1,
            player1_score,
            player2,
            player2_score,
            round,
        ).build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = w3.eth.account.sign_transaction(transaction, settings.PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # イベントをキャッチしてタイムスタンプを取得
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        logs = contract.events.MatchCreated().process_receipt(receipt)
        match_id = logs[0]["args"]["matchId"]
        created_at = logs[0]["args"]["createdAt"]

        return match_id, tx_hash.hex(), created_at

    except Exception as e:
        print(f"Error saving match to blockchain: {e}")
        return None, None, None


def get_matches_from_blockchain(
    match_id=None, tournament_id=None, user_id=None, round=None
):
    w3 = get_contract()
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_hardhat_compiled_contract()["abi"],
    )

    def match_to_dict(match):
        return {
            "id": match[0],
            "tournament_id": match[1],
            "created_at": match[2],
            "player1": match[3],
            "player1_score": match[4],
            "player2": match[5],
            "player2_score": match[6],
            "is_active": match[7],
            "round": match[8],
        }

    if match_id:
        match = contract.functions.getMatch(int(match_id)).call()
        matches = match_to_dict(match)
    elif tournament_id:
        matches = contract.functions.getMatchesByTournament(int(tournament_id)).call()
        matches = [match_to_dict(match) for match in matches]
    elif user_id:
        matches = contract.functions.getMatchesByUserId(user_id, True, 0, 100).call()
        matches = [match_to_dict(match) for match in matches]
    # elif round and tournament_id:
    #     matches = contract.functions.getMatchesByRound(
    #         int(round), int(tournament_id), True, 0, 100
    #     ).call()
    else:
        matches = contract.functions.getAllMatches(True, 0, 100).call()
        matches = [match_to_dict(match) for match in matches]
    return matches


def delete_match_from_blockchain(match_id):
    w3 = get_contract()
    contract = w3.eth.contract(
        address=settings.CONTRACT_ADDRESS,
        abi=get_hardhat_compiled_contract()["abi"],
    )

    account = w3.eth.account.from_key(settings.PRIVATE_KEY)

    try:
        transaction = contract.functions.deleteMatch(match_id).build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = w3.eth.account.sign_transaction(transaction, settings.PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        return tx_hash

    except Exception as e:
        print(f"Error deleting match from blockchain: {e}")
        return None
