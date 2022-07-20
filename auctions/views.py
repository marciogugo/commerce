from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid
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
            listing_title = request.POST['listingTitle']
            listing_content = request.POST['listingContent']
            listing_price = request.POST["listingPrice"]
            listing_stock = request.POST["listingStock"]
            listing_status = request.POST["listingStatus"]
            listing_image_url = request.POST["listingImageURL"]
            listing_image_file = request.FILES["listingImageFile"]
            listing_startDate = format.get_format(request.POST["listingStartDate"],'DATETIME_FORMAT')
            listing_endDate = format.get_format(request.POST["listingEndDate"],'DATETIME_FORMAT')

            print("Request: ", request.POST)

            # Attempt to create new listing
            try:
                listing = Listing()
                listing.listing_title = listing_title
                listing.listing_content = listing_content
                listing.listing_price = listing_price
                listing.listing_stock = listing_stock
                listing.listing_status = listing_status
                listing.listing_start_date = listing_startDate
                listing.listing_end_date = listing_endDate
                listing.listing_image_url = listing_image_url
                listing.listing_image_file = listing_image_file

                #frame.src = '{{MEDIA_URL}}{{form.listingImageFile}}';

                print("Listing: ", listing)

                listing.save()
            except IntegrityError:
                context = {
                    'form': form,
                    'message': 'Error while saving listing.',
                }
                return render(request, "auctions/new_listing.html", context)
            return HttpResponseRedirect(reverse("listings"))

    print('aqui fora ')

    context= {
        'form': form
    }

    print("contexto ", context)

    return render(request, "auctions/new_listing.html", context=context)


def listings(request):
    form = AuctionForm()

    listings = Listing.objects.all()

    context= {
        'form': form,
        'listings': listings,
    }

    return render(request, "auctions/listings.html", context=context)


@login_required
def watchlist(request):
    context= {
    }

    return render(request, "auctions/index.html", context=context)
