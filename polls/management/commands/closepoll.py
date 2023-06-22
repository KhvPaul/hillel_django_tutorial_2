from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int, choices=[1, 4, 5], help="User's ID")
        parser.add_argument("poll_ids", nargs="+", type=int)
        parser.add_argument(
            "-d",
            "--delete",
            help="Delete poll instead of closing it",
        )

    def handle(self, *args, **options):

        # print(f"user id: {options.get('user_id')}")
        for id in options.get("poll_ids"):
            self.stdout.write(self.style.ERROR(f"Poll closed: {id}"))
        #     print(f"poll id: {id}")
        # print(options.get("delete"))

    def handle(self, *args, **options):
        users_queryset = User.objects.filter(id_in=options.get("user_id"))
        if users_queryset.filter(is_superuser=True).exists():
            self.stdout.write(self.style.ERROR("ERROR: Superuser can't be deleted"))
        else:
            users_queryset.delete()
        self.stdout.write(self.style.SUCCESS("User successfully deleted"))