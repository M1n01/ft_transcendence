from django.core.management.base import BaseCommand

from tournament.tasks import hello_world


class Command(BaseCommand):
    def handle(self, *args, **options):  # type: ignore
        print("====== START =================")
        hello_world.apply_async(args=())  # type: ignore

        print("====== END   =================")
