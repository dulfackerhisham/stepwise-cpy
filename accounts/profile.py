from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from . models import Profile
from django.contrib import messages
from orders.forms import AddressForm





@login_required(login_url='logIn')
def user_profile(request):
    order_items = Order.objects.filter(user=request.user).order_by("-id")

    address = Profile.objects.filter(user=request.user)

    if request.method == 'POST':
        address_form = AddressForm(request.POST)

        if address_form.is_valid():


            new_address = Profile.objects.create(user=request.user)

            new_address.fname = address_form.cleaned_data['fname']
            new_address.lname = address_form.cleaned_data['lname']
            new_address.phone = address_form.cleaned_data['phone']
            new_address.email = address_form.cleaned_data['email']
            new_address.country = address_form.cleaned_data['country']
            new_address.address = address_form.cleaned_data['address']
            new_address.city = address_form.cleaned_data['city']
            new_address.state = address_form.cleaned_data['state']
            new_address.pincode = address_form.cleaned_data['pincode']
            new_address.save()

            messages.success(request, "Address Added Successfully")
            return redirect('user_profile')
        else:
            # messages.warning(request, "Fill all the fields")
            return redirect('user_profile')

    

    context = {
        'order_items': order_items,
        'address': address,
    }

    return render(request, "myAccount.html", context)

def order_detail(request, id):
    order_items = Order.objects.get(user=request.user, id=id)
    order_product = OrderItem.objects.filter(order= order_items)

    context = {
        'order_product': order_product
    }

    return render(request, "orderDetail.html", context)

def make_default_address(request):
    """
    updating Profile(address) Model status to True and False,
    one of the user address will be then default address to place a order
    """
    id = request.GET['id']
    Profile.objects.update(status=False)
    Profile.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})


