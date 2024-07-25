from django.contrib import admin
from. models import *

# Register your models here.

class ProductGalleryAdmin(admin.TabularInline):
    model = ProductItemGallery

class ProductItemAdmin(admin.ModelAdmin):
    inlines = [ProductGalleryAdmin]
    list_display = ['product_id', 'category_id', 'gender', 'size_id', 'color_id', 'price']
    readonly_fields = ['createdDate', 'modifiedDate', 'slug']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

    # def delete_model(self, request, obj):
    #     # Check if there are related images in the ProductItemGallery
    #     if obj.productitemgallery_set.exists():
    #     # If there are images, delete only the images and not the entire ProductItem
    #         obj.productitemgallery_set.all().delete()
    #     else:
    #     # If there are no images, delete the entire ProductItem
    #         obj.delete()

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Brand)
# admin.site.register(Gender)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductItemGallery)
admin.site.register(Coupon_code)
admin.site.register(Product_Review, ProductReviewAdmin)


