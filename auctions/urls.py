from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("redirect_auction", views.redirect_auction, name="redirect_auction"),
    path("listings", views.listings, name="listings"),
    path("comments", views.comments, name="comments"),
    path("categories", views.categories, name="categories"),
    path("new_listing", views.new_listing, name="new_listing"),
]
