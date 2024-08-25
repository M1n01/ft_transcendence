import os

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

    def email(self, user):
        # email_code_dict[to_address] = code

        to_address = user.email
        secret = user.app_secret
        last_login = user.last_login
        # twilio = TwoFA()

        totp = pyotp.TOTP(secret)
        code = totp.at(last_login)
        email_api_key = os.environ["BREVO_API_KEY"]
        email_sender_address = os.environ["BREVO_SENDER_ADDRESS"]
        # email_api_key = os.environ["BREVO_API_KEY"]
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = email_api_key
        sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        subject = f"42Pongの認証コード:{code}"
        sender = {"name": "42PongGame", "email": email_sender_address}
        html_content = (
            "<html><body><h1>"
            + f"This is my first transactional email2 Code:{code}"
            + "</h1></body></html>"
        )
        to = [{"email": to_address}]
        params = {"parameter": "My param value", "subject": "New Subject"}
        # send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            html_content=html_content,
            sender=sender,
            subject=subject,
            params=params,
        )

        # try:
        #    # Brevo側でrejectされてもここではerror判定ができない。
        #    # message_idを利用して別途APIを利用すれば判定できるが、時間がかかる上に不安定
        #    api_response = api_instance.send_transac_email(send_smtp_email)
        #    res_dict = ast.literal_eval(str(api_response))
        #    # message_id = res_dict["message_id"]
        # except ApiException as e:
        #    return False

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

    def verify_email(self, user, code):

        secret = user.app_secret
        last_login = user.last_login
        totp = pyotp.TOTP(secret)

        if code == totp.verify(code, last_login):
            return True
        return False

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
