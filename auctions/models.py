from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f'{self.username}'

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    creationDate = models.DateField(auto_now_add=True)
    image = models.URLField(blank=True)
    # category. Field.choises could be useful
    # currentPrice IntegerField
    # active BooleanField
    # winner User Puede ser nulo. Dependiente de la de arriba

    def __str__(self):
        return f'{self.title} {self.creationDate}'