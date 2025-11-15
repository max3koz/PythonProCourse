from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
	path("", views.visits_view, name="visits-view"),
	path("products/", views.product_list, name="product-list"),
	path("cart/", views.cart_view, name="cart-view"),
	path("cart/add/<int:product_id>/", views.cart_add, name="cart-add"),
	path("cart/remove/<int:product_id>/", views.cart_remove,
	     name="cart-remove"),
	path("cart/clear/", views.cart_clear, name="cart-clear"),
	path("analytics/top-products/",
	     views.top_products_by_sales,
	     name="top-products"),
	path("products-with-sales/",
	     views.product_list_with_sales,
	     name="product-list-with-sales"),
]
