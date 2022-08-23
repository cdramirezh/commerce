from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f'{self.username}'

class Auction(models.Model):
    title = models.CharField(max_length=64)
    # description
    # creationDate
    # image
    # category
    # currentPrice
    # active
    # winner

    def __str__(self):
        return f'{self.title}'