from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse

from products.models import ProductItem

from .models import Wishlist

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='logIn')
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)

    context = {'wishlist': wishlist}

    return render(request, "wishlist.html", context)


def add_to_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('id'))

            product_item = get_object_or_404(ProductItem, id=prod_id)

            product_check = ProductItem.objects.get(id=prod_id)
            if product_check:
                if(Wishlist.objects.filter(user=request.user, product=prod_id)):
                    return JsonResponse({'status': "Product Alreacy in Wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product=product_item)
                    return JsonResponse({'status': "Product Added to Wishlist"})
                    
        else:
            return JsonResponse({'status': "Login to continue"})

    return JsonResponse({'status': "Login To Add Product To Wishlist"})

# def delete_wishlist(request):
#     if request.method == 'POST':
#         prod_id = int(request.POST.get('id'))
#         if(Wishlist.objects.filter(user=request.user, product=prod_id)).exists():
#             wishlist = Wishlist.objects.get(user=request.user, product=prod_id)
#             wishlist.delete()
#             return JsonResponse({'status': "Product Removed From Wishlist"})
#         else:
#             return JsonResponse({'status': "Product does not exist"})

#     return redirect('/')

def delete_wishlist(request):
    if request.method == 'POST':
        wish_id = int(request.POST.get('id'))
        try:
            wish_item = Wishlist.objects.get(id=wish_id, user=request.user)
            wish_item.delete()
            return JsonResponse({'status': "Wishlist item removed"})
        except Wishlist.DoesNotExist:
            return JsonResponse({'status': "Wishlist item not found"})
    return JsonResponse({'status': "Invalid request"})