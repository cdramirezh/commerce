from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionForm
from .models import User, Auction, Bid


def index(request):
    return render(request, "auctions/index.html", {
        'auctions': Auction.objects.exclude(is_active=False).all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create_auction(request):

    if (request.method == 'POST'):
        
        auction_form = AuctionForm(request.POST)
        
        if auction_form.is_valid():
            auction_form.save()
            return render(request, "auctions/index.html")

        return render(request, "auctions/create_auction.html", {
            'form': auction_form,
            'message': 'Invalid form'
        })

    else:
        form = AuctionForm()
        return render(request, "auctions/create_auction.html", {
            'form': form
        })


def auction_page(request,auction_id):
    #Ensure the requested auction exists
    try:
        auction = Auction.objects.get(id=auction_id)    
    except ObjectDoesNotExist:
        return render(request, "auctions/auction_page.html", {
            'message': 'There was a problem getting the requested auction'
        })

    #Ensure the user is logged In
    try:
        auction_in_watchlist = auction in request.user.watchlist.all()
        
    except AttributeError:
        return render(request, "auctions/auction_page.html", {
            'auction': auction
        }) 

    #Define watchlist button message
    if auction_in_watchlist: watchlist_message = 'Remove from Watchlist'
    else: watchlist_message = 'Add to Watchlist'
    
    min_bid_value = auction.price + 1

    return render(request, "auctions/auction_page.html", {
        'auction': auction,
        'watchlist_message': watchlist_message,
        'min_bid_value': min_bid_value
    })

@login_required(login_url='login')
def toggle_watchlist(request, auction_id):

    try:
        auction = Auction.objects.get(id=auction_id)
    except ObjectDoesNotExist:
        return render(request, "auctions/auction_page.html", {
            'message': 'There was a problem getting the requested auction'
        })

    watchlist = request.user.watchlist.all()

    if auction in watchlist :
        request.user.watchlist.remove(auction)
    else:
        request.user.watchlist.add(auction)

    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

@login_required(login_url='login')
def bid(request, auction_id):

    if request.method == 'POST':
        
        # Ensure User has not changed the amount input name
        try:
            amount = int(request.POST['amount'])
        except:
            #Implement something better, like redirecting to auction_page
            # with an error message on the bid form
            return render(request, "auctions/auction_page.html", {
                'message': 'Error in bid amount Field'
            })

        user = request.user

        try:
            auction = Auction.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

        bid = Bid(amount=amount,user=user,auction=auction)
        try:
            bid.clean()
        except ValidationError:
            # Error should be presented in auction url.
            # Error message should be on the bid input itself
            return render(request, "auctions/auction_page.html", {
                'message': 'Error in bid amount'
            })
        bid.save()

    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))