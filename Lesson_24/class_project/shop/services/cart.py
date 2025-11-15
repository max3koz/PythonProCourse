from __future__ import annotations

from django.http import HttpRequest
from shop.types import CartDict

SESSION_KEY = "cart"


class CartService:
	"""
	A service for managing a shopping cart in a session.
	"""
	
	def __init__(self, request: HttpRequest) -> None:
		self.request = request
		self._ensure_cart()
	
	def _ensure_cart(self) -> None:
		"""Ensures the existence of a cart structure in the session."""
		if SESSION_KEY not in self.request.session:
			self.request.session[SESSION_KEY] = {}
	
	def get_cart(self) -> CartDict:
		"""Returns the current cart as a dictionary product_id -> quantity."""
		return dict(self.request.session.get(SESSION_KEY, {}))
	
	def add(self, product_id: int, quantity: int = 1) -> None:
		"""
		Adds a product to the cart or increases the quantity.
		Args:
			product_id: product identifier
			quantity: number of units added
		"""
		cart: CartDict = self.request.session.get(SESSION_KEY, {})
		cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
		self.request.session[SESSION_KEY] = cart
		self.request.session.modified = True
	
	def remove(self, product_id: int) -> None:
		"""Removes product from cart by product_id."""
		cart: CartDict = self.request.session.get(SESSION_KEY, {})
		cart.pop(str(product_id), None)
		self.request.session[SESSION_KEY] = cart
		self.request.session.modified = True
	
	def clear(self) -> None:
		"""Emptys the entire trash."""
		self.request.session[SESSION_KEY] = {}
		self.request.session.modified = True
