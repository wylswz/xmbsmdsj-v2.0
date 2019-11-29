from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import json


class Command(BaseCommand):
    help = "Init the super user"



    def handle(self, *args, **options):
        SUPERUSER_NAME_ = input("Username")
        SUPERUSER_EMAIL_ = input("Email")
        SUPERUSER_PASSWORD_ = input("Password")
        SUPERUSER_PASSWORD_R = input("Repeat Password")
        if SUPERUSER_PASSWORD_ == SUPERUSER_PASSWORD_R:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(SUPERUSER_NAME_, SUPERUSER_EMAIL_, SUPERUSER_PASSWORD_)
            else:
                User.objects.filter(is_superuser=True).delete()
                User.objects.create_superuser(SUPERUSER_NAME_, SUPERUSER_EMAIL_, SUPERUSER_PASSWORD_)
            print("init")