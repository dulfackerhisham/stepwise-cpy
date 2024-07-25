from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . models import Cart
from accounts.models import Profile
from django.contrib import messages
from products.models import Coupon_code



@login_required(login_url='logIn')
def checkout_view(request):
    applied_coupon_code = request.session.get('applied_coupon')
    print(f"{applied_coupon_code} checkout view is called")


    subtotal = 0

    cart = Cart.objects.filter(user=request.user.id)
    for item in cart:
        item.total_price = item.product.price * item.qty
        subtotal += item.total_price

    try:
        active_address = Profile.objects.get(user=request.user, status=True)
    except:
        # messages.warning(request, "There might be multiple addresses, only one should be Activated.")
        active_address = None


    coupon_discount = 0
    valid_coupon = None
    invalid_coupon = None
    applied_coupon = None

    if applied_coupon_code:
        try:
            valid_coupon = "Are Applicable on Current Order !"
            applied_coupon = Coupon_code.objects.get(code=applied_coupon_code, active=True)
            coupon_discount = applied_coupon.discount
        except Coupon_code.DoesNotExist:
            # applied_coupon = None
            invalid_coupon = "Invalid Coupon Code !"
            applied_coupon_code = None

    #calculating the total amount after reducing discount
    updated_total = subtotal - (subtotal * coupon_discount / 100)

    #fetch active coupon codes
    available_coupons = Coupon_code.objects.filter(active=True)

    

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'active_address': active_address,
        'updated_total': updated_total,
        'valid_coupon': valid_coupon,
        'applied_coupon': applied_coupon,
        'invalid_coupon': invalid_coupon,
        'available_coupons': available_coupons,
    }
    return render(request, "checkout.html", context)