from django.apps import AppConfig
from django.conf import settings


class ScoreKeeperConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pong.score_keeper"

    def ready(self):
        from .eth import deploy_contract

        contract_address = deploy_contract()
        if contract_address:
            settings.PONG_SCORE_CONTRACT_ADDRESS = contract_address
            print(f"Deployed PongScore contract at: {contract_address}")
        else:
            print("Failed to deploy PongScore contract")
