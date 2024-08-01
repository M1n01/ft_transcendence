import os
from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# from __future__ import print_function

import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import ast
import time
import urllib.parse


DEV_SMS = True

email_code_dict = {}


class TwoFA:
    """
    2段階認証の各サービスへのインターフェース
    """

    sms_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    sms_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    sms_service_token = os.environ["TWILIO_SERVICE_SID"]

    def sms(self, phone_number):
        client = Client(self.sms_account_sid, self.sms_auth_token)
        phone_number = "+81" + phone_number[1:]
        print(f"{phone_number=}")
        if DEV_SMS:
            return True
        try:
            verification = client.verify.v2.services(
                self.sms_service_token
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
        client = Client(self.sms_account_sid, self.sms_auth_token)
        print(f"{phone_number=}")
        print(f"{code=}")
        # return False

        if DEV_SMS:
            return True
        try:
            verification_check = client.verify.v2.services(
                self.sms_service_token
            ).verification_checks.create(to=phone_number, code=code)
        except TwilioRestException:
            print("Error")
            return False

        print(verification_check.status)
        if verification_check.status == "pending":
            return False
            print("Error")
        return True

    def email(self, to_address, code):
        email_code_dict[to_address] = code
        print(f"save {to_address=}")
        print(f"save {code=}")
        email_api_key = os.environ["BREVO_API_KEY"]
        email_sender_address = os.environ["BREVO_SENDER_ADDRESS"]
        # email_api_key = os.environ["BREVO_API_KEY"]
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = email_api_key
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        subject = f"42Pongの認証コード:{code}"
        sender = {"name": "42PongGame", "email": email_sender_address}
        html_content = f"<html><body><h1>This is my first transactional email2 Code:{code}</h1></body></html>"
        to = [{"email": to_address}]
        params = {"parameter": "My param value", "subject": "New Subject"}
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject,
            params=params,
        )

        try:
            # Brevo側でrejectされてもここではerror判定ができない。
            # message_idを利用して別途APIを利用すれば判定できるが、時間がかかる上に不安定
            api_response = api_instance.send_transac_email(send_smtp_email)
            res_dict = ast.literal_eval(str(api_response))
            message_id = res_dict["message_id"]
        except ApiException as e:
            print(f"Brevo Error:{e}")
            return False

        # check
        """
        cnt = 0
        while cnt > 5:
            time.sleep(2.5)
            cnt = cnt + 1
            url = (
                "https://api.brevo.com/v3/smtp/statistics/events?limit=1&offset=0&messageId="
                + urllib.parse.quote(message_id)
                + "&sort=desc"
            )
            headers = {"accept": "application/json", "api-key": email_api_key}
        """

        return True

    def verify_email(self, email_address, code):
        print(f"verify_email:{email_address=}")
        print(f"verify_email:{code=}")
        print(f"verify_email:{email_code_dict[email_address]=}")
        if code == str(email_code_dict[email_address]):
            print("equal")
            return True
        print("NG")
        return False
