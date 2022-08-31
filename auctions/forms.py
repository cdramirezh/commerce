from django.forms import ModelForm
from .models import Auction, Comment

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        exclude = ['creator','is_active','winner']

# There is no a Form for Bid because I wanted to set the min_value
# of the 'amount' field corresponding to the 'amount' attribute of the Auction Model
# every time I created a new BidForm,
# but I couldn't find a way to do it with the Django ModelForm class,
# So I did it manually

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['date','user','auction']