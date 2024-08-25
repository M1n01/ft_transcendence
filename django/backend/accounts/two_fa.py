import os
import ast
from sib_api_v3_sdk.rest import ApiException


# from django.conf import settings

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


# import time
import sib_api_v3_sdk

# from sib_api_v3_sdk.rest import ApiException

# import time
# import urllib.parse
import pyotp

# SMSサービスを一時的に無効にする
# SMSサービスは有料なので、使用を制限したいため
# これがTrueであると、認証コードは何を入力しても通る
DEV_SMS = True

# email_code_dict = {}


class TwoFA:
    """
    2段階認証の各サービスへのインターフェース
    """

    sms_account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    sms_auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    sms_service_token = os.environ["TWILIO_SERVICE_SID"]

    def sms(self, user):

        phone_number = user.country_code + user.phone
        client = Client(self.sms_account_sid, self.sms_auth_token)
        # phone_number = "+81" + phone_number[1:]
        if DEV_SMS:
            return True
        try:
            client.verify.v2.services(self.sms_service_token).verifications.create(
                to=phone_number, channel="sms"
            )
        except TwilioRestException:
            return False

        return True
        # return response.json()

    def verify_sms(self, user, code):
        phone_number = user.country_code + user.phone
        # account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        # auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(self.sms_account_sid, self.sms_auth_token)
        # return False

        if DEV_SMS:
            return True
        try:
            verification_check = client.verify.v2.services(
                self.sms_service_token
            ).verification_checks.create(to=phone_number, code=code)
        except TwilioRestException:
            return False

        if verification_check.status == "pending":
            return False
        return True

    def email(self, user, time):
        # email_code_dict[to_address] = code
        print("email No.1")

        to_address = user.email
        secret = user.app_secret
        # last_login = user.last_login
        print("email No.2")
        print(f"email No.2 {to_address=}")
        print(f"email No.2 {secret=}")
        print(f"email No.2 {time=}")
        # twilio = TwoFA()

        totp = pyotp.TOTP(secret)
        print("email No.3")
        code = totp.at(time)
        print("email No.4")
        email_api_key = os.environ["BREVO_API_KEY"]
        print("email No.5")
        email_sender_address = os.environ["BREVO_SENDER_ADDRESS"]
        print("email No.3")
        # email_api_key = os.environ["BREVO_API_KEY"]
        configuration = sib_api_v3_sdk.Configuration()
        print("email No.4")
        configuration.api_key["api-key"] = email_api_key
        print(f"email No.5 {email_api_key=}")
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        print("email No.6")

        subject = f"42Pongの認証コード:{code}"
        print(f"email No.7 {email_sender_address=}")
        sender = {"name": "42PongGame", "email": email_sender_address}
        print("email No.8")
        html_content = (
            "<html><body><h1>"
            + f"This is my first transactional email Code:{code}"
            + "</h1></body></html>"
        )
        print(f"email No.9:{html_content=}")
        to = [{"email": to_address}]
        print("email No.10")
        # params = {"parameter": "My param value", "subject": "New Subject"}
        # params = {"parameter": "My param value", "subject": "New Subject"}

        params = {"contact": {"CODE": "******"}}

        print(f"email No.11:{params=}")
        print(f"email No.11:{to=}")
        print(f"email No.11:{sender=}")
        print(f"email No.11:{subject=}")
        # send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject,
            params=params,
        )
        print("email No.12")

        try:
            # Brevo側でrejectされてもここではerror判定ができない。
            # message_idを利用して別途APIを利用すれば判定できるが、時間がかかる上に不安定
            api_response = api_instance.send_transac_email(send_smtp_email)
            res_dict = ast.literal_eval(str(api_response))
            message_id = str(res_dict["message_id"])
            print(f"{message_id=}")

            # message_id = res_dict["message_id"]
        except ApiException as e:
            print(e)
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
        print("email No.13")

        return True

    def verify_email(self, user, time, code):

        secret = user.app_secret
        print(f"{secret=}")
        print(f"{code=}")
        # last_login = user.last_login
        totp = pyotp.TOTP(secret)

        return totp.verify(code, time)

    def make_uri(self, email, secret):

        totp = pyotp.TOTP(secret)
        # secret = totp.secret

        # QRコードのURI生成
        uri = totp.provisioning_uri(name=email, issuer_name="42 Pong Game")
        return uri

    def app(self, user):
        email = user.email
        secret = user.app_secret
        return self.make_uri(email, secret)

    def verify_app(self, user, code):
        secret = user.app_secret
        totp = pyotp.TOTP(secret)
        totp.now()

        if code == totp.now():
            return True
        return False
