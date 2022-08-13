from socket import TCP_NODELAY
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone 

from auctions.choices import CATEGORY_CHOICES

from .models import User, Listing, Watchlist, Bid
from .forms import ListingForm, RegisterForm, AuctionForm

from django.db.models import Max
from django.db.models import F, Q, Value
from django.db.models.functions import Greatest, Coalesce

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
                listing.listing_id = listing.pk
                listing.listing_category = listing_category
                listing.listing_title = listing_title
                listing.listing_content = listing_content
                listing.listing_price = listing_price
                listing.listing_image_file = listing_image_file
                listing.save()
            except IntegrityError:
                context = {
                    'form': form,
                    'message': 'Error while saving listing.',
                }
                return render(request, "auctions/new_listing.html", context=context)
            return HttpResponseRedirect(reverse("index"))

    context= {
        'form': form
    }
    return render(request, "auctions/new_listing.html", context=context)


def listings(request):
    form = AuctionForm()

    if request.method == 'POST':
        form = AuctionForm(request.POST)

        if not form.is_valid():
            return render(request, "auctions/index.html", {
                "message": "Fill out the requested bid value."
            })
        else:
            listingId = request.POST['currentId']
            listingBid = request.POST['currentBid'+listingId]

            print("Preço autal " + listingBid)

            listing = Listing.objects.get(listing_id = listingId)

            if listingBid != 0:
                user = get_object_or_404(User.objects.filter(pk=request.session['user_id']))
                
                bid = Bid()
                bid.user = user
                bid.product = listing
                #if bid.bid_starting_value == 0:
                #    bid.bid_starting_value = listingBid
                bid.bid_current_value = listingBid
                #bid.bid_start_date_time = timezone.now()
                #bid.bid_finish_date_time = None
                bid.bid_finished = 'N'
                bid.save()

            listings = Listing.objects.values()

            if 'user_id' in request.session:
                bookmarks = Watchlist.objects.values().filter(user_id=request.session['user_id'])
            else:
                bookmarks = Watchlist.objects.values()

            #bids = Bid.objects.values().filter(product__in = listings.values('listing_id'))
            bids = Bid.objects.values().filter(product__in = listings.values('listing_id')).aggregate(Max('bid_current_value'))
            
            highest_bid = bids.get('bid_current_value__max')
    else:
        listings = Listing.objects.values()

        if 'user_id' in request.session:
            bookmarks = Watchlist.objects.values().filter(user_id=request.session['user_id'])
        else:
            bookmarks = Watchlist.objects.values()

        # correto bids = Bid.objects.values().filter(product__in = listings.values('listing_id'))

        bids = Bid.objects.values().filter(product__in = listings.values('listing_id')).distinct()
        bids = bids.annotate(max=Max('bid_current_value', filter=Q(product__in = listings.values('listing_id'))))

        #bids = bids.annotate(max=Max('bid_current_value'))
        #maxBids = Bid.objects.values().filter(
        #    product__in = listings.values('listing_id')).aggregate(
        #        max = Coalesce(Max('bid_current_value'),listings.values('listing_price')))

        #maxBids = Bid.objects.values().filter(
        #    product__in = listings.values('listing_id')).aggregate(
        #        max = Coalesce(Max('bid_current_value'),listings.values('listing_price')))

        print("As bids:", bids.values('product_id'))
        print("As bids:",bids.values('max','product_id'))
        #print("As bids:",bids.get('max'))
        #print("Max1 ", maxBids)
        #print("Max2 ", maxBids.get('max'))
        #print("As bids:",bids.get('max'))

        highest_bid = 0 #bids.get('bid_current_value__max')

    context= {
        'form': form,
        'listings': listings,
        'categories': CATEGORY_CHOICES,
        'is_bookmarked': False,
        'bookmarks': bookmarks,
        'bookmark_count': bookmarks.count,
        'bids': bids,
        'highest_bid': highest_bid,
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
