from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja import Schema
from ninja.responses import Response

from .models import Product, CartItem, Order, OrderItem
from .schemas import ProductIn, ProductOut, CartItemIn, CartItemOut, OrderOut

shop_router = Router(tags=["shop"])


class OrderStatusIn(Schema):
	status: str


# ------------------ Products ------------------

@shop_router.post("/products/", response=ProductOut)
@login_required
def create_product(request, payload: ProductIn):
	"""Create a new product."""
	product = Product.objects.create(**payload.dict())
	return Response(ProductOut.from_orm(product), status=201)


@shop_router.get("/products/", response=list[ProductOut])
@login_required
def list_products(request):
	"""List all products."""
	return Product.objects.all()


@shop_router.get("/products/{product_id}", response=ProductOut)
@login_required
def get_product(request, product_id: int):
	"""Retrieve a single product by ID."""
	return get_object_or_404(Product, id=product_id)


@shop_router.put("/products/{product_id}", response=ProductOut)
@login_required
def update_product(request, product_id: int, payload: ProductIn):
	"""Update product details."""
	product = get_object_or_404(Product, id=product_id)
	for attr, value in payload.dict().items():
		setattr(product, attr, value)
	product.save()
	return product


@shop_router.delete("/products/{product_id}")
@login_required
def delete_product(request, product_id: int):
	"""Delete a product."""
	product = get_object_or_404(Product, id=product_id)
	product.delete()
	return {"success": True}


# ------------------ Cart ------------------

@shop_router.post("/cart/", response=CartItemOut)
@login_required
def add_to_cart(request, payload: CartItemIn):
	"""Add a product to the user's cart."""
	user = request.user if request.user.is_authenticated else User.objects.first()
	product = get_object_or_404(Product, id=payload.product_id)
	
	cart_item, created = CartItem.objects.get_or_create(user=user,
	                                                    product=product)
	cart_item.quantity += payload.quantity
	cart_item.save()
	
	data = {
		"id": cart_item.id,
		"product_id": cart_item.product.id,
		"quantity": cart_item.quantity,
	}
	return Response(data, status=201)


@shop_router.delete("/cart/{item_id}")
@login_required
def remove_from_cart(request, item_id: int):
	"""Remove a product from the user's cart."""
	user = request.user if request.user.is_authenticated else User.objects.first()
	item = get_object_or_404(CartItem, id=item_id, user=user)
	item.delete()
	return {"success": True}


# ------------------ Orders ------------------

@shop_router.post("/orders/", response=OrderOut)
@login_required
def create_order(request):
	"""Create an order."""
	user = request.user if request.user.is_authenticated else User.objects.first()
	cart_items = CartItem.objects.filter(user=user)
	
	order = Order.objects.create(user=user, status="pending")
	for item in cart_items:
		OrderItem.objects.create(order=order, product=item.product,
		                         quantity=item.quantity)
	cart_items.delete()
	
	data = {
		"id": order.id,
		"status": order.status,
	}
	return Response(data, status=201)


@shop_router.put("/orders/{order_id}")
@login_required
def update_order_status(request, order_id: int, payload: OrderStatusIn):
	"""Update the status of an order."""
	user = request.user if request.user.is_authenticated else User.objects.first()
	order = get_object_or_404(Order, id=order_id, user=user)
	order.status = payload.status
	order.save()
	data = {"success": True, "status": order.status}
	return Response(data, status=200)
