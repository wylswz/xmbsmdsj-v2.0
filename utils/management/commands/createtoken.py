from django.core.management.base import BaseCommand
from utils.models import Token

class Command(BaseCommand):
    help = "create an API token"

    def handle(self, *args, **options):
        token = input("Your token:")
        token_2 = input("Repeat your token:")
        if token == token_2:
            Token.create_token(token)
        else:
            print("Please make sure tokens are same!")

