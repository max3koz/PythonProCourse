from __future__ import annotations
from django.db.models import QuerySet
from shop.models import Product

def optimized_products_qs() -> QuerySet[Product]:
	"""
	Returns a QuerySet of products with an optimized selection of related categories.
	Uses select_related('category') to avoid N+1 queries.
	"""
	return Product.objects.select_related("category")