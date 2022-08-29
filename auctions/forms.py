from django.forms import ModelForm
from .models import Auction, Bid

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            'title',
            'description',
            'price',
            'image',
            'category'
        ]
