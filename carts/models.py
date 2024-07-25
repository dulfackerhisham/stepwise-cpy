from django.db import models
from accounts.models import Account
from products.models import ProductItem
import uuid

# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    qty  = models.PositiveIntegerField()
    createdDate = models.DateTimeField(auto_now_add=True)