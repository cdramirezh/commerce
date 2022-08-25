from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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
    category = models.CharField(max_length=2, choices=CATEGORY_CHOISES, blank=True)
    
    #When a new bid to the auction is created, the price is updated
    price = models.PositiveIntegerField(help_text='Not to exceed 2147483647!')
    def set_price(self, price):
        self.price = price
        self.save()

    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_auctions")

    def close(self, winner):
        self.winner=winner
        self.set_active_status(False)
        self.save()
    
    def set_active_status(self,status):
        self.is_active = status
        self.save()

    # When updating winner, the following constrain is applied: 
    # if winner is not null: is_active = False        
    def clean(self):
        if self.winner is not None:
            self.set_active_status(False)
            
    def __str__(self):
        return f'{self.title} {self.creationDate} {self.price}$ {self.is_active} {self.winner}'

class Comment(models.Model):
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        content_len = len(self.content)
        preview_thresshold = 12
        if content_len >= preview_thresshold:
            content_preview = self.content[0:preview_thresshold] + '...'
        else:
            content_preview = self.content
        return f'{self.user}: -> {self.auction.title}: {content_preview}'

class Bid(models.Model):
    
    amount = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} bids {self.amount} to {self.auction.title}'

    def clean(self):
        # When creating a Bid, the following constrains are implemented:
        if self.amount <= self.auction.price:
            raise ValidationError(f'Amount should be greater than {self.auction.price}')
        else:
            self.auction.set_price(self.amount)
        # Do not create bids on closed auctions
        if not self.auction.is_active:
            raise ValidationError(f'Cannot create bids on closed auctions')