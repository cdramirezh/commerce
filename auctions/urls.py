from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auction", views.create_auction, name='create_auction'),
    path("auction/<int:auction_id>", views.auction_page, name='auction'),
    path("toggle_watchlist/<int:auction_id>", views.toggle_watchlist, name='toggle_watchlist'),
    path("bid/<int:auction_id>", views.bid, name='bid'),
    path("close/<int:auction_id>", views.close_auction, name='close')
]
