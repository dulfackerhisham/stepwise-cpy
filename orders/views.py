from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . models import Order,OrderItem
from carts.models import Cart
from products.models import ProductItem
from django.contrib import messages
from accounts.models import Profile
from . constants import PAYMENT_TYPE_RAZORPAY
from .forms import AddressForm
from django.db import transaction

from products.models import Coupon_code
#celery
# from .task import send_email_task
import random

# Create your views here.

#transaction.atomic !Done!
@login_required(login_url='logIn')
def place_order(request):
    """
    takes a request of COD or razorpay and does the validation
    and of address field if uses old address it gets it and do 
    the payment integration and saves to the Order and OrderItem models

    """
    if request.method == 'POST':

        address_form = AddressForm(request.POST)

        if address_form.is_valid():

            # Start a database transaction block
            with transaction.atomic():
                neworder = Order()
                neworder.user = request.user
                neworder.payment_mode = request.POST.get('payment_mode')
                neworder.payment_id = request.POST.get('payment_id')

                #FORM VALIDATION done !Done!
                # Check if a Profile for the user exists, and create/update it
                address, created = Profile.objects.get_or_create(user=request.user, status=True)


                address.fname = address_form.cleaned_data['fname']
                address.lname = address_form.cleaned_data['lname']
                address.phone = address_form.cleaned_data['phone']
                address.email = address_form.cleaned_data['email']
                address.country = address_form.cleaned_data['country']
                address.address = address_form.cleaned_data['address']
                address.city = address_form.cleaned_data['city']
                address.state = address_form.cleaned_data['state']
                address.pincode = address_form.cleaned_data['pincode']
                address.save()

                #set the applied coupon code in the order
                applied_coupon_code = request.session.get('applied_coupon', None)
                # print(f"Applied Coupon Code: {applied_coupon_code}")
                if applied_coupon_code:
                    try:
                        coupon = Coupon_code.objects.get(code=applied_coupon_code, active=True)
                        # print(f"Coupon Status: {coupon.active}")
                        neworder.applied_coupon = coupon
                        # print("Coupon Applied to Order")
                    except Coupon_code.DoesNotExist:
                        neworder.applied_coupon = None
                        # print("Coupon Not Found")

                neworder.address = address


        
                # # TODO : remove for loop move to DB !Done!



                tracking_number = genearate_tracking_number(request.user)
                neworder.tracking_no = tracking_number
                neworder.save()

                neworderitems = Cart.objects.filter(user=request.user)

                # Create a list of OrderItem objects to be created in bulk
                order_items = []

                for item in neworderitems:
                    #preparing data for OrderItem creation

                    order_item_data = {
                        'order': neworder,
                        'product': item.product,
                        'price': item.product.price,
                        'quantity': item.qty,
                        # TODO: remove total amount !Done!
                    }

                    # Append the data to the list
                    order_items.append(OrderItem(**order_item_data))

                    #decreasing product quantity from available stock
                    # TODO: locking mechanism => reduce & bd locker !Done!
                    orderproduct = ProductItem.objects.select_for_update().get(id=item.product.id)
                    if orderproduct.stock >= item.qty:
                        orderproduct.stock -= item.qty
                        orderproduct.save()
                    else:
                        return JsonResponse({'error': 'Not enough stock'})
                    
            # Clear the applied_coupon session
            if 'applied_coupon' in request.session:
                del request.session['applied_coupon']

            # Clear the list of applied coupons in the session
            request.session['applied_coupons'] = []


            # Use a database transaction for the bulk create operation
            OrderItem.objects.bulk_create(order_items)


            #clearing user's cart
            Cart.objects.filter(user=request.user).delete()


            pay_mode = request.POST.get('payment_mode')
            if (pay_mode == PAYMENT_TYPE_RAZORPAY):
                # TODO: translation languages
                # send_email_task.delay(request.user.id,  neworder.id)
                # print(f"worked {send_email_task} ")
                return JsonResponse({'status': 'Your Order has been placed successfully'})
                # return redirect("payment-confirmation")

            else:
                # send_email_task.delay(request.user.id,  neworder.id)
                messages.success(request, "Your Order has been placed successfully")
                return redirect("payment-confirmation")

        
        else:
            return JsonResponse({'error': 'Form validation failed. Return back to checkout Page'})

    # return render(request, "confirmation.html")

    #TODO admin actions on ordered items



@login_required(login_url='logIn')
def razorpay_check(request):
    """
    getting total amount of all products to integrate
    razorpay.
    """
    cart = Cart.objects.filter(user=request.user)

    subtotal = 0
    for item in cart:
        totalprice = item.product.price * item.qty
        subtotal += totalprice

    # Check if a coupon is applied
    applied_coupon_code = request.session.get('applied_coupon', None)

    if applied_coupon_code:
        # Try to get the coupon or set discounted_price to subtotal
        try:
            coupon = Coupon_code.objects.get(code=applied_coupon_code, active=True)
            # Apply the coupon discount to the subtotal
            subtotal -= subtotal * coupon.discount / 100
        except Coupon_code.DoesNotExist:
            # If the coupon is not found, ignore it
            pass

    return JsonResponse({'subtotal': subtotal})

def genearate_tracking_number(user):
    tracking_number = f"{user.username}-{random.randint(1111111,9999999)}"
    return tracking_number




def payment_confirmation(request):
    """retrieving a users latest order details"""

    latest_order = Order.objects.filter(user=request.user).order_by('-created_at').first()

    if latest_order:
        order_items = OrderItem.objects.filter(order=latest_order)
        address = Profile.objects.filter(user=request.user, status=True)

        context = {
            'order': latest_order,
            'order_items': order_items,
            'address': address,
        }
        return render(request, "confirmation.html", context)
    else:
        messages.error(request, "No order found")
        return redirect('/')

#digital ocean,AWS
#gitignore, readme

