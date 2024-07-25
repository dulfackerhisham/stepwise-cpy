from django.db import models
from accounts.models import Account
from products.models import ProductItem
from accounts.models import Profile
from products.models import Coupon_code
from django.db.models import Sum, F


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    address = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatus = {
        ('pending', 'pending'),
        ('out for shipping', 'out for shipping'),
        ('completed', 'completed'),
    }
    status = models.CharField(max_length=150, choices=orderstatus, default='Pending')
    tracking_no = models.CharField(max_length=250, null=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    applied_coupon = models.ForeignKey(Coupon_code, on_delete=models.SET_NULL, null=True,blank=True)


    def __str__(self):
        return f"{self.id} {self.tracking_no}"
    
    def calculate_total_price(self):
        """
        calculating the total_price of all product with the quantity respectively from cart model
        """
        #TODO remove for loop and use aggregriate method !DONE!

        total_price = self.user.cart_set.aggregate(
        # F for getting value of appropriate fields
            total_price=Sum(F('product__price') * F('qty'), output_field=models.FloatField())
        )['total_price'] or 0.0

        # total_price = 0
        # for cart_item in self.user.cart_set.all():
        #     total_price += cart_item.product.price * cart_item.qty

        if self.applied_coupon:
            total_price -= (total_price * self.applied_coupon.discount / 100)
        return total_price
    
    def save(self, *args, **kwargs):
        """
        Set the total_price before saving the order.

        """


        self.total_price = self.calculate_total_price()
        super(Order, self).save(*args, **kwargs)
    
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return f" {self.product} {self.order.tracking_no}"
    

