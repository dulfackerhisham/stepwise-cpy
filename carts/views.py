from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect

from . models import Cart
from products.models import ProductItem
from django.contrib.auth.decorators import login_required

from products.models import Coupon_code

# Create your views here.

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('id'))

            print(prod_id)

            # Get the ProductItem instance or return 404 if not found
            product_item = get_object_or_404(ProductItem, id=prod_id)

            #at first we are checking if there is product exist with this id
            product_check = ProductItem.objects.get(id=prod_id)
            if (product_check):
                #if user have already added product to cart
                if (Cart.objects.filter(user=request.user.id, product=prod_id)):
                    return JsonResponse({'status': "Product Already in Cart"})
                else:
                    #if product is not in cart we will add product to cart
                    prod_qty = int(request.POST.get('qty'))

                    #reverse the logic
                    if product_check.stock >= prod_qty:
                        Cart.objects.create(user=request.user, product=product_item, qty=prod_qty)
                        return JsonResponse({'status': "Product Added Successfully"})
                    else:
                        return JsonResponse({'status': "Product Out Of Stock "})
                        

            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})

    return redirect('/')

    # return render(request, "cart.html")

@login_required(login_url='logIn')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user.id).order_by('-createdDate')

    subtotal = 0
    for item in cart:
        item.total_price = item.product.price * item.qty
        subtotal += item.total_price

    #Coupon code
    coupon = None
    valid_coupon = None
    invalid_coupon = None

    if request.method == "GET":
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_code.objects.get(code=coupon_code)
                valid_coupon = "Are Applicable on Current Order !"
            except:
                invalid_coupon = "Invalid Coupon Code !"


    context = {'cart': cart,
               'subtotal': subtotal,
               'coupon': coupon,
               'valid_coupon': valid_coupon,
               'invalid_coupon': invalid_coupon,
               }

    return render(request, "cart.html", context)

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('id'))
        prod_qty = int(request.POST.get('qty'))

        if Cart.objects.filter(user=request.user, product=prod_id).exists():
            cart = Cart.objects.get(product=prod_id, user=request.user)
            p_stock = cart.product.stock
            
            if p_stock < prod_qty:
                return JsonResponse({'status': "Product Have " + str(p_stock) + " Stocks"}) #cant see the error
            else:
                print(prod_qty)
                cart.qty = prod_qty
                cart.save()

                 # Calculate the new total price
                new_total_price = cart.product.price * cart.qty

                # Recalculate the subtotal
                subtotal = 0
                cart_items = Cart.objects.filter(user=request.user.id)
                for item in cart_items:
                    item.total_price = item.product.price * item.qty
                    subtotal += item.total_price
                return JsonResponse({'status': "Updated Successfully", 'new_total_price': new_total_price, 'subtotal': subtotal})
        else:
            return JsonResponse({'status': "Product not found in cart"})

    return redirect('/')


def deletecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('id'))
        if(Cart.objects.filter(user=request.user, product=prod_id)).exists():
            cart = Cart.objects.get(product=prod_id, user=request.user)
            cart.delete()
            return JsonResponse({'status': "Product Removed From Cart"})
        else:
            return JsonResponse({'status': "Product not Removed From Cart"})
    return redirect('/')


