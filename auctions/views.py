from itertools import product
from socket import TCP_NODELAY
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone 

from auctions.choices import CATEGORY_CHOICES

from .models import User, Listing, Watchlist, Bid, Comment
from .forms import ListingForm, RegisterForm, AuctionForm, CategoriesForm

from django.db.models import Max
from django.db.models import F, Q, Value
from django.db.models.functions import Greatest, Coalesce
from django.db.models.expressions import RawSQL

def index(request):
    return listings(request)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse("listings"))
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
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "auctions/register.html", {
                "message": "Fill out all the requested fields."
            })
        else:
            first_name = request.POST['registerFirstName']
            last_name = request.POST['registerLastName']
            username = request.POST["registerUsername"]
            email = request.POST["registerEmail"]

            # Ensure password matches confirmation
            password = request.POST["registerPassword"]
            confirmation = request.POST["registerConfPassword"]

            if password != confirmation:
                context = {
                    'form': form,
                    'message':'Passwords must match.',
                }
                return render(request, "auctions/register.html", context)

            # Attempt to create new user
            try:
                user = User.objects.create_user(username=username,
                                                first_name=first_name, 
                                                last_name=last_name, 
                                                email=email, 
                                                password=password)
                user.save()
                request.session['user_id'] = user.id
            except IntegrityError:
                context = {
                    'form': form,
                    'message': 'Username already taken.',
                }
                return render(request, "auctions/register.html", context)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    context = {
        "form": form,
    }
    return render(request, "auctions/register.html", context=context)


@login_required
def new_listing(request):
    form = ListingForm()
    bookmarks = Watchlist.objects.filter(user_id=request.session['user_id'])
    user = get_object_or_404(User.objects.filter(pk=request.session['user_id']))

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)

        if not form.is_valid():
            return render(request, "auctions/new_listing.html", {
                "message": "Fill out all the requested fields."
            })
        else:
            listing_category = request.POST['listingCategory']
            listing_title = request.POST['listingTitle']
            listing_content = request.POST['listingContent']
            listing_price = request.POST["listingPrice"]
            listing_image_file = request.FILES["listingImageFile"]

            # Attempt to create new listing
            try:
                listing = Listing()
                listing.user = user
                listing.listing_id = listing.pk
                listing.listing_category = listing_category
                listing.listing_title = listing_title
                listing.listing_content = listing_content
                listing.listing_price = listing_price
                listing.listing_image_file = listing_image_file
                listing.listing_finished = 'N'
                listing.save()
            except IntegrityError:
                context = {
                    'form': form,
                    'message': 'Error while saving listing.',
                }
                return render(request, "auctions/new_listing.html", context=context)
            return HttpResponseRedirect(reverse("index"))

    context= {
        'form': form,
        'bookmark_count': bookmarks.count,
    }
    return render(request, "auctions/new_listing.html", context=context)


def redirect_auction(request):
    form = AuctionForm()

    if request.method == 'POST':
        pass
        # print("entrou post")
        # print("nem vai precisar do post")
        # form = AuctionForm(request.POST)

        # if not form.is_valid():
        #     return render(request, "auctions/index.html", {
        #         "message": "Fill out the requested bid value."
        #     })
        # else:
        #     listingId  = request.POST['currentId']
        #     listingBid = request.POST['currentBid'+listingId]

        #     listing = Listing.objects.get(listing_id = listingId)
        #     user = get_object_or_404(User.objects.filter(pk=request.session['user_id']))

        #     if listingBid != '-1':
        #         bid = Bid()
        #         bid.user = user
        #         bid.product = listing
        #         bid.bid_current_value = listingBid
        #         bid.bid_finished = 'N'
        #         bid.save()
        #     else:
        #         listing.listing_finished = 'S'
        #         listing.save()

        #     listings = Listing.objects.values()

        #     if 'user_id' in request.session:
        #         bookmarks = Watchlist.objects.values().filter(user_id=request.session['user_id'])
        #     else:
        #         bookmarks = Watchlist.objects.values()

        #     bids = Bid.objects.raw('select listing_id as id, '+
        #                            '       listing_price, '+
        #                            '       coalesce((select max(bid_current_value) '+
        #                            '                   from auctions_bid '+
        #                            '                  where product_id = listing_id),listing_price) as highest_bid '+
        #                            '  from auctions_listing')
            
        #     highest_bid = 0

        #     comments = Comment.objects.all()
    else:
        listing  = get_object_or_404(Listing.objects.filter(pk=request.GET.get('product_id')))
        comments = Comment.objects.filter(product=request.GET.get('product_id'))

        if 'user_id' in request.session:
            bookmarks = Watchlist.objects.values().filter(user_id=request.session['user_id'])
        else:
            bookmarks = Watchlist.objects.values()

        bids = Bid.objects.raw('select listing_id as id, '+
                               '       user_id, '+
                               '       listing_finished, '+
                               '       listing_price, '+
                               '       coalesce((select max(bid_current_value) '+
                               '                   from auctions_bid '+
                               '                  where product_id = listing_id),listing_price) as highest_bid, '+
                               '       coalesce((select user_id '+ 
                               '                   from (select user_id, max(bid_current_value) from auctions_bid where product_id = listing_id)),0) as winner '+
                               '  from auctions_listing')

        highest_bid = 0
    context= {
        'form': form,
        'listing': listing,
        'categories': CATEGORY_CHOICES,
        'is_bookmarked': False,
        'bookmarks': bookmarks,
        'bookmark_count': bookmarks.count,
        'bids': bids,
        'highest_bid': highest_bid,
        'comments': comments,
    }
    return render(request, "auctions/auction.html", context=context)


def listings(request):
    form = AuctionForm()

    if request.method == 'POST':
        form = AuctionForm(request.POST)

        if not form.is_valid():
            return render(request, "auctions/index.html", {
                "message": "Fill out the requested bid value."
            })
        else:
            listingId  = request.POST['currentId']
            listingBid = request.POST['currentBid'+listingId]

            listing = Listing.objects.get(listing_id = listingId)
            user = get_object_or_404(User.objects.filter(pk=request.session['user_id']))

            if request.POST['addComments'] == 'False':
                if listingBid != '-1':
                    bid = Bid()
                    bid.user = user
                    bid.product = listing
                    bid.bid_current_value = listingBid
                    bid.bid_finished = 'N'
                    bid.save()
                else:
                    listing.listing_finished = 'S'
                    listing.save()

            listings = Listing.objects.values()

            if 'user_id' in request.session:
                bookmarks = Watchlist.objects.values().filter(user_id=request.session['user_id'])
            else:
                bookmarks = Watchlist.objects.values()

            if request.POST['addComments'] == 'True':
                comment = Comment()
                comment.user = user
                comment.product = listing
                comment.comment_content = request.POST['itemComment']
                comment.save()

            bids = Bid.objects.raw('select listing_id as id, '+
                                '       listing_price, '+
                                '       coalesce((select max(bid_current_value) '+
                                '                   from auctions_bid '+
                                '                  where product_id = listing_id),listing_price) as highest_bid '+
                                '  from auctions_listing')
        
            highest_bid = 0

            comments = Comment.objects.all()
    else:
        listings = Listing.objects.values()

        if 'user_id' in request.session:
            bookmarks = Watchlist.objects.values().filter(user_id=request.session['user_id'])
        else:
            bookmarks = Watchlist.objects.values()

        bids = Bid.objects.raw('select listing_id as id, '+
                               '       user_id, '+
                               '       listing_finished, '+
                               '       listing_price, '+
                               '       coalesce((select max(bid_current_value) '+
                               '                   from auctions_bid '+
                               '                  where product_id = listing_id),listing_price) as highest_bid, '+
                               '       coalesce((select user_id '+ 
                               '                   from (select user_id, max(bid_current_value) from auctions_bid where product_id = listing_id)),0) as winner '+
                               '  from auctions_listing')

        highest_bid = 0

        comments = Comment.objects.all()
    context= {
        'form': form,
        'listings': listings,
        'categories': CATEGORY_CHOICES,
        'is_bookmarked': False,
        'bookmarks': bookmarks,
        'bookmark_count': bookmarks.count,
        'bids': bids,
        'highest_bid': highest_bid,
        'comments': comments,
    }
    return render(request, "auctions/index.html", context=context)


@login_required
def watchlist(request):
    form = AuctionForm()

    bookmarks = Watchlist.objects.filter(user_id=request.session['user_id'])
    listings = Listing.objects.values().filter(listing_id__in = bookmarks.values('product_id'))
    bids = Bid.objects.values().filter(product__in = bookmarks.values('product_id'))
    highest_bid = 0

    context= {
        'form': form,
        'listings': listings,
        'bookmarks': bookmarks,
        'bookmark_count': bookmarks.count,
        'bids': bids,
        'highest_bid': highest_bid,
    }
    return render(request, "auctions/watchlist.html", context=context)


@login_required
def add_watchlist(request):
    form = AuctionForm()

    # Attempt to create new watchlist
    try:
        user = get_object_or_404(User.objects.filter(pk=request.session['user_id']))
        listing = get_object_or_404(Listing.objects.filter(pk=request.GET.get('product_id')))

        watchlist = Watchlist();
        watchlist.user = user
        watchlist.product = listing
        watchlist.save()
    except IntegrityError:
        context = {
            'form': form,
            'message': 'Error while saving to watchlist.',
        }
        return render(request, "auctions/index.html", context=context)
    return HttpResponseRedirect(reverse("listings"))


@login_required
def remove_watchlist(request):
    form = AuctionForm()

    # Attempt to create remove from watchlist
    try:
        user = get_object_or_404(User.objects.filter(pk=request.session['user_id']))
        listing = get_object_or_404(Listing.objects.filter(pk=request.GET.get('product_id')))

        watchlist = Watchlist.objects.filter(user=user.id,product=listing.listing_id);
        watchlist.delete()
    except IntegrityError:
        context = {
            'form': form,
            'message': 'Error while removing from watchlist.',
        }
        return render(request, "auctions/index.html", context=context)
    return HttpResponseRedirect(reverse("listings"))


def categories(request):
    form = CategoriesForm()

    listings = Listing.objects.values()
    bookmarks = []

    if 'user_id' in request.session:
        bookmarks = Watchlist.objects.filter(user_id=request.session['user_id'])

    if request.method == 'POST':
        form = CategoriesForm(request.POST)

        if 'categoriesCategory' in request.POST:
            if request.POST['categoriesCategory'] == '-Empty-':
                listings = Listing.objects.values()
            else:
                listings = Listing.objects.values().filter(listing_category = request.POST['categoriesCategory'])

    context= {
        'form': form,
        'listings': listings,
        'bookmarks': bookmarks,
        'bookmark_count': bookmarks.count,
    }
    return render(request, "auctions/categories.html", context=context)
