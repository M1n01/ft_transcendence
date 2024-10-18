import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now


class DeleteInactiveUsersCommand(BaseCommand):
    help = "一定期間ログインしていないユーザーを削除する"

    def handle(self, *args, **kwargs):
        User = get_user_model()  # FtUserモデルを取得
        threshold_date = now() - datetime.timedelta(
            minutes=10
            # days=365
        )  # 1年間ログインしていないユーザーを対象
        inactive_users = User.objects.filter(last_login__lt=threshold_date)

        # count, _ = inactive_users.delete()
        # self.stdout.write(self.style.SUCCESS(f"{count} FtUsers deleted."))
        if inactive_users.exists():
            for user in inactive_users:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Inactive user: {user.email}, Last login: {user.last_login}"
                    )
                )
        else:
            self.stdout.write(self.style.WARNING("No inactive users found."))
