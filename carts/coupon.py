from django.shortcuts import  redirect
from products.models import Coupon_code
from django.contrib import messages
from django.contrib.auth.decorators import login_required




@login_required(login_url='logIn')
def apply_coupon(request):
    if request.method == 'GET':
        coupon_code = request.GET.get("coupon_code")
        # print("apply_coupon function is called")
        print(coupon_code)

        # Get a list of applied coupons
        applied_coupons = request.session.get('applied_coupons', [])

        if coupon_code in applied_coupons:
            # If the coupon code is in the list of applied coupons, show an error message
            # print("Coupon has already been used")
            messages.error(request, "Coupon code has already been used")
        else:
            try:
                # Retrieving the entered coupon
                coupon = Coupon_code.objects.get(code=coupon_code, active=True)

                if coupon:
                    # If a valid coupon is found, store it in the session
                    request.session['applied_coupon'] = coupon_code

                    # Add the coupon code to the list of applied coupons
                    applied_coupons.append(coupon_code)
                    request.session['applied_coupons'] = applied_coupons

                    return redirect('checkout')

            except Coupon_code.DoesNotExist:
                # print("Coupon does not exist")
                messages.error(request, "Invalid Coupon")
                return redirect('checkout')

    # Handle other HTTP methods as needed
    return redirect('checkout')





