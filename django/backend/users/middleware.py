from users.models import UserActionLog


class UserActionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            url = request.path
            status_code = response.status_code
            method = request.method

            UserActionLog.objects.create(
                user=request.user, url=url, status_code=status_code, method=method
            )

        return response
