from __future__ import annotations

from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .models import Product
from .services.analytics import optimized_products_qs
from .services.cart import CartService


def visits_view(request: HttpRequest) -> HttpResponse:
	"""
	Displays the page and sets/updates the 'visits' cookie — the number of visits.
	Logic:
	- reads the value of the 'visits' cookie (default 0)
	- increments it by 1
	- returns the response and sets the cookie with security parameters
	"""
	raw = request.COOKIES.get("visits", "0")
	try:
		visits = int(raw)
	except ValueError:
		visits = 0
	visits += 1
	
	response = render(request,
	                  "shop/product_list.html",
	                  {"visits": visits})
	response.set_cookie(
		"visits",
		str(visits),
		max_age=7 * 24 * 60 * 60,
		httponly=True,
		samesite="Lax")
	return response


def cart_view(request: HttpRequest) -> HttpResponse:
	"""Displays the cart: converts product_id -> quantity to a list of products."""
	cart = CartService(request).get_cart()
	product_ids = [int(pid) for pid in cart.keys()]
	
	products = Product.objects.select_related("category").filter(
		id__in=product_ids)
	
	items = []
	total = 0
	for p in products:
		qty = cart.get(str(p.id), 0)
		subtotal = p.price * qty
		total += subtotal
		items.append({"product": p, "qty": qty, "subtotal": subtotal})
	
	return render(request, "shop/cart.html", {"items": items, "total": total})


def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
	"""Adds an item to the cart and returns it to the cart."""
	get_object_or_404(Product, id=product_id)
	cart = CartService(request)
	cart.add(product_id, quantity=1)
	return redirect("shop:cart-view")


def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
	"""Removes an item from the cart and returns it to the cart."""
	cart = CartService(request)
	cart.remove(product_id)
	return redirect("shop:cart-view")


def cart_clear(request: HttpRequest) -> HttpResponse:
	"""Clears the basket and returns to the basket.	"""
	cart = CartService(request)
	cart.clear()
	return redirect("shop:cart-view")


def product_list(request: HttpRequest) -> HttpResponse:
	"""
	A list of products with categories.
	Demonstrates N+1 optimization via select_related('category').
	"""
	products = optimized_products_qs()
	return render(request,
	              "shop/product_list.html",
	              {"products": products,
	               "visits": request.COOKIES.get("visits", "0")})


def product_list_with_sales(request: HttpRequest) -> HttpResponse:
	"""
	List of products with sales prefetch (for aggregation examples in the template).
	"""
	products = Product.objects.select_related("category").prefetch_related(
		"sales")
	return render(request,
	              "shop/product_list.html",
	              {"products": products})


def top_products_by_sales(request):
	"""Top 10 products by sales volume with total sales."""
	qs = (
		Product.objects
		.select_related("category")
		.annotate(
			sales_count=Count("sales"),
			quantity_total=Coalesce(Sum("sales__quantity"), 0),
		)
		.annotate(
			# тут ми обгортаємо вираз у ExpressionWrapper і явно задаємо output_field
			sales_total=ExpressionWrapper(
				F("price") * F("quantity_total"),
				output_field=DecimalField(max_digits=12, decimal_places=2)
			)
		)
		.order_by("-sales_count", "-sales_total")[:10]
	)
	
	return render(request, "shop/product_list.html", {"products": qs})
