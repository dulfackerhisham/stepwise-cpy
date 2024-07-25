from django.urls import path
from .views import index, productList, productDetail, filter_product, ajax_add_review

urlpatterns = [
    path("", index, name="home"),
    path("products/", productList, name="productList"),
    path("product-detail/<str:slug>/", productDetail, name="productDetail"),

    #ajax for product filter
    path("filter-product/", filter_product, name="filter-product"),

    #add review
    path("add-review/<int:id>/", ajax_add_review, name="add-review"),
]

