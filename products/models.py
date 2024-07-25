from django.db import models
from django.utils import timezone

from django.utils.text import slugify
from accounts.models import Account
# Create your models here.

gender_choices = (
        ('M', 'Men'),
        ('F', 'Women'),
    )

RATING = (
    (1, "⭐☆☆☆☆"),
    (2, "⭐⭐☆☆☆"),
    (3, "⭐⭐⭐☆☆"),
    (4, "⭐⭐⭐⭐☆"),
    (5, "⭐⭐⭐⭐⭐"),
)


class Product(models.Model):
    title        = models.CharField(max_length=200, unique=True)
    description  = models.TextField(max_length=1000)


    def __str__(self):
        return self.title

class Category(models.Model):
    category_choices = (
        ('boots', 'Boots'),
        ('casuals', 'Casuals'),
        ('formal', 'Formal'),
        ('sports', 'Sports'),
    )

    name = models.CharField(max_length=100, unique=True, choices=category_choices)
    image = models.ImageField(upload_to="category", default="No file choosen")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()  # Convert to lowercase before saving
        super(Category, self).save(*args, **kwargs)

class Size(models.Model):
    size_value = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.size_value)

class Color(models.Model):
    color_value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.color_value
    
    def save(self, *args, **kwargs):
        self.color_value = self.color_value.lower()  # Convert to lowercase before saving
        super(Color, self).save(*args, **kwargs)   # Call the parent class's save() method

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.brand_name
    
    def save(self, *args, **kwargs):
        self.brand_name = self.brand_name.lower()  # Convert to lowercase before saving
        super(Brand, self).save(*args, **kwargs)   # Call the parent class's save() method

# class Gender(models.Model):

#     gender_choices = (
#         ('M', 'Men'),
#         ('F', 'Women'),
#     )
#     gender_value = models.CharField(max_length=1, choices=gender_choices, unique=True)

#     def __str__(self):
#         return self.gender_value

class ProductItem(models.Model):
    product_id      = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_item")
    category_id     = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    size_id         = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    color_id        = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    brand_id        = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # gender_id   = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    gender          = models.CharField(max_length=1, choices=gender_choices)
    img             = models.ImageField(upload_to="img")
    price           = models.IntegerField()
    slug            = models.SlugField(max_length=300, unique=True)
    stock           = models.PositiveIntegerField()
    createdDate     = models.DateTimeField(auto_now_add=True)
    modifiedDate    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.gender)

    
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        # Concatenate fields to create the slug
        if not self.slug:
            self.slug = slugify(f'{self.brand_id.brand_name} {self.product_id.title} {self.gender} {self.size_id.size_value} {self.color_id.color_value}')
        super(ProductItem, self).save(*args, **kwargs)
        
   
    
class ProductItemGallery(models.Model):
    productItem = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True, related_name="p_images")
    image = models.ImageField(upload_to="image")

    def __str__(self):
        return f'{self.image}'
    

class Coupon_code(models.Model):
    code = models.CharField(max_length=150)
    discount = models.IntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    

class Product_Review(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.product_id.title
    
    def get_rating(self):
        return self.rating