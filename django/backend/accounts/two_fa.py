import os
from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

DEV_SMS = True


class TwoFA:
    """
    2段階認証の各サービスへのインターフェース
    """

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    service_token = os.environ["TWILIO_SERVICE_SID"]

    def sms(self, phone_number):

        client = Client(self.account_sid, self.auth_token)

        phone_number = "+81" + phone_number[1:]
        print(f"{phone_number=}")
        if DEV_SMS:
            return True
        try:
            verification = client.verify.v2.services(
                self.service_token
            ).verifications.create(to=phone_number, channel="sms")
        except TwilioRestException:
            # print("Twilio Error")
            return False

        print(verification.sid)
        return True
        # return response.json()

    def verify_sms(self, phone_number, code):
        phone_number = "+81" + phone_number[1:]
        # account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        # auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(self.account_sid, self.auth_token)
        print(f"{phone_number=}")
        print(f"{code=}")
        # return False

        if DEV_SMS:
            return True
        try:
            verification_check = client.verify.v2.services(
                self.service_token
            ).verification_checks.create(to=phone_number, code=code)
        except TwilioRestException:
            print("Error")
            return False

        print(verification_check.status)
        if verification_check.status == "pending":
            return False
            print("Error")
        return True
