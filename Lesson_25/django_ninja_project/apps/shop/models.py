from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
	"""Represents a product in the e-commerce store."""
	name: str = models.CharField(max_length=255)
	description: str = models.TextField()
	price: float = models.DecimalField(max_digits=10, decimal_places=2)
	stock: int = models.PositiveIntegerField(default=0)
	
	def __str__(self) -> str:
		return self.name


class CartItem(models.Model):
	"""Represents a product added to a user's cart."""
	user: User = models.ForeignKey(User, on_delete=models.CASCADE)
	product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity: int = models.PositiveIntegerField(default=1)
	
	def __str__(self) -> str:
		return f"{self.user.username} - {self.product.name}"


class Order(models.Model):
	"""Represents an order placed by a user."""
	STATUS_CHOICES = [
		("pending", "Pending"),
		("processing", "Processing"),
		("shipped", "Shipped"),
		("delivered", "Delivered"),
	]
	
	user: User = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at: str = models.DateTimeField(auto_now_add=True)
	status: str = models.CharField(max_length=20, choices=STATUS_CHOICES,
	                               default="pending")
	
	def __str__(self) -> str:
		return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
	"""Represents a product inside an order."""
	order: Order = models.ForeignKey(Order, on_delete=models.CASCADE,
	                                 related_name="items")
	product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity: int = models.PositiveIntegerField(default=1)
	
	def __str__(self) -> str:
		return f"{self.order.id} - {self.product.name}"
