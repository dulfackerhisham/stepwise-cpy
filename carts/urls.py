from django.urls import path
from .views import addtocart, viewcart, updatecart, deletecart
from .checkout import checkout_view
from .coupon import apply_coupon

urlpatterns = [
    path("add_to_cart/", addtocart, name='add_to_cart'),
    path("", viewcart, name='cart'),
    path("update-cart/", updatecart, name='updatecart'),
    path("delete-cart/", deletecart, name='deletecart'),
    path("checkout/", checkout_view, name='checkout'),
    path("apply-coupon/", apply_coupon, name='apply_coupon'),
    
]

