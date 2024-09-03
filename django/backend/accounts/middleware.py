from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.exceptions import SessionInterrupted
from django.utils.cache import patch_vary_headers

# from django.utils.deprecation import MiddlewareMixin
from django.utils.http import http_date

# from .models import FtUser, FtTmpUser

# from django.contrib.auth.models import AnonymousUser
import jwt
import time
from datetime import datetime, timezone, timedelta

# from importlib import import_module


class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        tmp_session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        session_key = tmp_session_key
        is_provisional_login = False
        jwt_decode = ""
        exp = ""
        user_id = "-1"
        try:
            if tmp_session_key is not None:
                jwt_decode = jwt.decode(
                    tmp_session_key,
                    getattr(settings, "SECRET_KEY", None),
                    leeway=5,  # 通信上の遅延で５秒遅くても大丈夫ないように
                    algorithms=["HS256"],
                )
                session_key = jwt_decode["session_key"]
                if "is_tmp" in jwt_decode:
                    is_provisional_login = jwt_decode["is_tmp"]
                if "exp" in jwt_decode:
                    exp = jwt_decode["exp"]
                if "sub" in jwt_decode:
                    user_id = jwt_decode["sub"]
        except jwt.ExpiredSignatureError:
            is_provisional_login = False
            # leeway+expで設定した時間を超過したらここに入る
            pass
        except jwt.exceptions.DecodeError:
            is_provisional_login = False
            # tmp_session_keyが編集されていたらここに入る
            pass
        request.session = self.SessionStore(session_key)
        request.session["is_provisional_login"] = is_provisional_login
        request.session["exp"] = exp
        request.session["user_id"] = user_id
        # request.session["jwt_decode"] = jwt_decode

    def process_response(self, request, response):
        try:
            accessed = request.session.accessed
            modified = request.session.modified
            empty = request.session.is_empty()
        except AttributeError:
            return response
        if settings.SESSION_COOKIE_NAME in request.COOKIES and empty:
            response.delete_cookie(
                settings.SESSION_COOKIE_NAME,
                path=settings.SESSION_COOKIE_PATH,
                domain=settings.SESSION_COOKIE_DOMAIN,
                samesite=settings.SESSION_COOKIE_SAMESITE,
            )
            patch_vary_headers(response, ("Cookie",))
        else:
            if accessed:
                patch_vary_headers(response, ("Cookie",))
            if (modified or settings.SESSION_SAVE_EVERY_REQUEST) and not empty:
                if request.session.get_expire_at_browser_close():
                    max_age = None
                    expires = None
                else:
                    max_age = request.session.get_expiry_age()
                    expires_time = time.time() + max_age
                    expires = http_date(expires_time)

                if response.status_code < 500:
                    try:
                        request.session.save()
                    except UpdateError:
                        raise SessionInterrupted(
                            "The request's session was deleted before the "
                            "request completed. The user may have logged "
                            "out in a concurrent request, for example."
                        )
                    # user = request.user
                    # is_provisional = True
                    id = ""
                    email = ""
                    is_provisional_login = False
                    exp = datetime.now(tz=timezone.utc) + timedelta(seconds=14400)
                    if "is_provisional_login" in request.session:
                        is_provisional_login = request.session["is_provisional_login"]
                        if (is_provisional_login is True) and (
                            "exp" in request.session
                        ):
                            exp = datetime.fromtimestamp(float(request.session["exp"]))
                            id = request.session["user_id"]
                        # email = user.email

                    jwt_session_key = jwt.encode(
                        {
                            "session_key": request.session.session_key,
                            "iss": "https://localhost",
                            "sub": id,
                            "email": email,
                            "is_tmp": is_provisional_login,
                            "exp": exp,
                            "nbf": datetime.now(tz=timezone.utc)
                            + timedelta(seconds=3),  # この時間より前に処理されたらエラーにする
                            "iat": datetime.now(tz=timezone.utc),
                            # "jti":"token-id" #必要なら使う
                        },
                        getattr(settings, "SECRET_KEY", None),
                        algorithm="HS256",
                    )
                    response.set_cookie(
                        settings.SESSION_COOKIE_NAME,
                        jwt_session_key,
                        max_age=max_age,
                        expires=expires,
                        domain=settings.SESSION_COOKIE_DOMAIN,
                        path=settings.SESSION_COOKIE_PATH,
                        secure=settings.SESSION_COOKIE_SECURE or None,
                        httponly=settings.SESSION_COOKIE_HTTPONLY or None,
                        samesite=settings.SESSION_COOKIE_SAMESITE,
                    )
        return response
