from django.urls import path
from . views import wishlist_view, add_to_wishlist, delete_wishlist

urlpatterns = [
    path('', wishlist_view, name="wishlist"),
    path('add_to_wishlist/', add_to_wishlist, name="add_to_wishlist"),
    path('delete-wishlist/', delete_wishlist, name="delete_wishlist"),
]