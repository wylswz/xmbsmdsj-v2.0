from django.db import models
from patent.settings import hash
# Create your models here.



class Token(models.Model):
    token = models.CharField(max_length=1000)

    @staticmethod
    def create_token(passphrase):
        existing = Token.objects.all().delete()
        new_token = Token()
        new_token.token = hash(passphrase)
        new_token.save()

    @staticmethod
    def get_token():
        try:
            token = Token.objects.all()[0].token
        except Exception as e:
            token = '85fd7c889f71cf105375595cddc06b9d38fc562cb69c54f8c165aa751d81b3d9'

        return token



