from . models import Category,Brand,Color,ProductItem
from django.db.models import Min, Max

def default(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    colors = Color.objects.all()

    min_max_price = ProductItem.objects.aggregate(Min("price"), Max("price"))

    return {
        'category': category,
        'brand': brand,
        'colors': colors,
        'min_max_price': min_max_price,
    }