from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from . models import ProductItem, Brand, Category, Size
from django.template.loader import render_to_string
from django.core.paginator import Paginator

from . models import Product_Review
from .forms import ProductReviewForm

from django.db.models import Count,Avg
from orders.models import OrderItem



# Create your views here.
def index(request):
    # user = request.user 
    try:
        # Get the brand named "Nike"
        # nike_brand = Brand.objects.get(brand_name__iexact='nike')

        # Get the last added product for the "Nike" brand
        last_added_product = ProductItem.objects.filter(brand_id__brand_name__iexact='adidas').latest('id')

    except Brand.DoesNotExist:
        # Handle the case if the brand "Nike" does not exist
        last_added_product = None

    unique_products = ProductItem.objects.order_by('product_id', 'brand_id', 'id').distinct('product_id', 'brand_id')
    

    categories = Category.objects.all()
    #do it in cache

    # Category = Category.objects.all()


    context = {
        'last_added_product': last_added_product,
        'products': unique_products,
        'categories': categories,
        # 'user': user
    }



    return render(request, "index.html", context)

def productList(request):

    #try to add select to fetch data from other tables(foriegn key)
    # unique_products = ProductItem.objects.order_by('product_id', 'brand_id', 'id').distinct('product_id', 'brand_id')
    unique_products = ProductItem.objects.distinct('product_id', 'brand_id')

   # Set the default sorting order
    default_sort = 'price_low'

    # Retrieving the selected sorting field from the URL
    sort_items = request.GET.get('sort', default_sort)

    # Query your products based on your needs
    if sort_items == 'price_low':
        products = ProductItem.objects.all().order_by('price')
    elif sort_items == 'price_high':
        products = ProductItem.objects.all().order_by('-price')
    else:
        products = ProductItem.objects.all()
        


    # Initialize paginator
    paginator = Paginator(unique_products, 3)  # 12 products per page

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)


    context = {
        # 'products': unique_products,
        'page': page,
        'products': products,
    }
    return render(request, "category.html", context)


def productDetail(request, slug):

    products = get_object_or_404(ProductItem, slug=slug)

    #Getting reviews related to a product
    reviews = Product_Review.objects.filter(product=products).order_by("-date")

    #getting average reviews
    average_rating = Product_Review.objects.filter(product=products).aggregate(rating=Avg('rating'))

    #product review form
    review_form = ProductReviewForm()

    #checking if the user has bought the product
    user_has_bought = False

    if request.user.is_authenticated:
        #checking if there is an order for the current user and product
        user_order = OrderItem.objects.filter(order__user=request.user, product=products)

        if user_order.exists():
            user_has_bought = True



    #making user to give one review only for a product
    make_review = True

    if request.user.is_authenticated:
        user_review_count = Product_Review.objects.filter(user=request.user, product=products).count()

        if user_review_count > 0:
            make_review = False

    context = {
        'product': products,
        'reviews': reviews,
        'make_review': make_review,
        'average_rating': average_rating,
        'review_form': review_form,
        'user_has_bought': user_has_bought,
    }

    return render(request, "single-product.html", context)


def ajax_add_review(request, id):
    product = ProductItem.objects.get(id=id)
    user = request.user

    review = Product_Review.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],

    )

    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    average_review = Product_Review.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'average_review': average_review,
        }
    )



def filter_product(request):
    categories = request.GET.getlist('category[]')
    brands     = request.GET.getlist('brand[]')
    # colors     = request.GET.getlist('color[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products   = ProductItem.objects.order_by("-id").distinct()

    # Apply price range filtering
    products = products.filter(price__gte=min_price, price__lte=max_price) #lte = less than or equal to

    if len(categories) > 0:
        products = products.filter(category_id__id__in = categories).distinct()

    if len(brands) > 0:
        products = products.filter(brand_id__id__in = brands).distinct()

    # if len(colors) > 0:
    #     products = products.filter(color_id__id__in = colors).distinct()

    data = render_to_string("ajax/product-list.html", {'products': products})

    return JsonResponse({"data": data})