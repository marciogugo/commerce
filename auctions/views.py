from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import User, Listing, Bid, Watchlist
from .forms import ListingForm, RegisterForm, AuctionForm

def index(request):
    return render(request, "auctions/index.html")


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
    return HttpResponseRedirect(reverse("listings"))


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
            listing_id =  request.POST['listingId']
            listing_title = request.POST['listingTitle']
            listing_content = request.POST['listingContent']
            listing_price = request.POST["listingPrice"]
            listing_image_file = request.FILES["listingImageFile"]

            # Attempt to create new listing
            try:
                listing = Listing()
                listing.listing_id = listing.pk
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
            return HttpResponseRedirect(reverse("listings"))

    context= {
        'form': form
    }
    return render(request, "auctions/new_listing.html", context=context)


def listings(request):
    form = AuctionForm()

    listings = Listing.objects.values()

    if 'user_id' in request.session:
        bookmarks = Watchlist.objects.values().filter(user_id=request.session['user_id'])
    else:
        bookmarks = Watchlist.objects.values()

    context= {
        'form': form,
        'listings': listings,
        'is_bookmarked': False,
        'bookmarks': bookmarks,
    }

    return render(request, "auctions/index.html", context=context)

@login_required
def watchlist(request):
    context= {
    }
    return render(request, "auctions/index.html", context=context)


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
    return HttpResponseRedirect(reverse(listings))


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
    return HttpResponseRedirect(reverse(listings))
