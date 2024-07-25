from django.db import models
from accounts.models import Account
from products.models import ProductItem

# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.product
