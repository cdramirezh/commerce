from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AuctionForm, CommentForm
from .models import Auction, Bid, Comment, User


def get_auction_number(request):
    try:
        auctions_in_watchlist = request.user.watchlist.all().count()
    except:
        auctions_in_watchlist = 0
    return auctions_in_watchlist

def index(request):
    return render(request, "auctions/index.html", {
        'auctions': Auction.objects.exclude(is_active=False).all(),
        'auctions_in_watchlist': get_auction_number(request)
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
            auction_form.instance.creator = request.user
            auction_form.save()
            return HttpResponseRedirect(reverse(index))

        return render(request, "auctions/create_auction.html", {
            'form': auction_form,
            'message': 'Invalid form',
            'auctions_in_watchlist': get_auction_number(request)
        })

    else:
        form = AuctionForm()
        return render(request, "auctions/create_auction.html", {
            'form': form,
            'auctions_in_watchlist': get_auction_number(request)
        })


def auction_page(request,auction_id):
    #Ensure the requested auction exists
    try:
        auction = Auction.objects.get(id=auction_id)    
    except ObjectDoesNotExist:
        return render(request, "auctions/auction_page.html", {
            'message': 'There was a problem getting the requested auction',
            'auctions_in_watchlist': get_auction_number(request)
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
    
    # Define minimun bid value
    min_bid_value = auction.price + 1

    # Define if the user is the one who created the listing
    # Any of the two following works
    user_is_creator = auction.creator == request.user
    user_is_creator = auction in request.user.created_auctions.all()

    #Define if the user is the winner
    user_is_winner = auction.winner == request.user

    # Get the comments
    comments = Comment.objects.all().filter(auction=auction_id)

    # Define a comment form
    comment_form = CommentForm()

    # Define number of bids already made of the auction
    # number_of_bids = Bid.objects.filter(auction=auction).count()
    number_of_bids = auction.bids.count()

    # Define if your bid is the current bid
    try: user_is_last_bidder = request.user == auction.bids.all().order_by('-amount')[0].user
    except: user_is_last_bidder = False

    return render(request, "auctions/auction_page.html", {
        'auction': auction,
        'watchlist_message': watchlist_message,
        'min_bid_value': min_bid_value,
        'user_is_creator': user_is_creator,
        'user_is_winner': user_is_winner,
        'comment_form': comment_form,
        'comments': comments,
        'auctions_in_watchlist': get_auction_number(request),
        'number_of_bids': number_of_bids,
        'user_is_last_bidder': user_is_last_bidder
    })

@login_required(login_url='login')
def toggle_watchlist(request, auction_id):

    try:
        auction = Auction.objects.get(id=auction_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

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
                'message': 'Error in bid amount Field',
                'auctions_in_watchlist': get_auction_number(request)
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
                'message': 'Error in bid amount',
                'auctions_in_watchlist': get_auction_number(request)
            })
        bid.save()

    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

@login_required(login_url='login')
def close_auction(request, auction_id):

    #Ensure the requested auction exists
    try:
        auction = Auction.objects.get(id=auction_id)    
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

    auction.close()
    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))


@login_required(login_url='login')
def add_comment(request, auction_id):

    if request.method == 'POST':

        # Make sure the auction exist
        try:
            auction = Auction.objects.get(id=auction_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("auction", args=(auction_id,)))

        comment_form = CommentForm(request.POST)

        user = request.user

        if comment_form.is_valid():
            comment_form.instance.user = user
            comment_form.instance.auction = auction
            comment_form.save()
        else:
            # This message should be pressented in the Auction Page, wiht the auction url
            return HttpResponse('Ivalid comment')
    return HttpResponseRedirect(reverse("auction", args=(auction_id,)))


@login_required(login_url='login')
def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/index.html", {
        'auctions': watchlist,
        'watchlist_view': True,
        'auctions_in_watchlist': watchlist.count()
    })

def categories(request):
    categories = Auction.CATEGORY_CHOISES
    return render(request, "auctions/categories.html", {
        'categories': categories,
        'auctions_in_watchlist': get_auction_number(request)
    })


def category(request, category):

    auctions = Auction.objects.all().filter(category=category).filter(is_active=True)

    category_h = ''
    for cat in Auction.CATEGORY_CHOISES:
        if cat[0] == category: category_h = cat[1]
        
    return render(request, "auctions/index.html", {
        'category_human_readable': category_h,
        'auctions': auctions,
        'auctions_in_watchlist': get_auction_number(request)
    })