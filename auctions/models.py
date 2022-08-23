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

    FASHION = 'FA'
    TOYS = 'TO'
    ELECTRONICS = 'EL'
    HOME = 'HO'
    CATEGORY_CHOISES = [
        (FASHION, 'Fashion'),
        (TOYS, 'Toys'),
        (ELECTRONICS, 'Electronics'),
        (HOME, 'Home')]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOISES)
    
    price = models.PositiveIntegerField(help_text='Not to exceed 2147483647!')
    is_active = models.BooleanField(default=True)
    # When updating winner, the following constrain To be implemented: 
    # if winner is not null: is_active = False
    winner = models.ForeignKey(User, on_delete= models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.title} {self.creationDate} {self.price}$ {self.is_active} {self.winner}'