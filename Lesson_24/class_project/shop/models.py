from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
	"""
	Product Category Model.
	Used to group products and demonstrate the select_related example.
	"""
	name: models.CharField = models.CharField(_("Назва"),
	                                          max_length=200,
	                                          unique=True)
	
	class Meta:
		verbose_name = _("Категорія")
		verbose_name_plural = _("Категорії")
	
	def __str__(self) -> str:
		return self.name


class Product(models.Model):
	"""
	Product model.
	Fields:
	- name: product name
	- price: current price
	- category: ForeignKey to Category (for example N+1 and select_related)
	"""
	name: models.CharField = models.CharField(_("Назва"),
	                                          max_length=255)
	price: models.DecimalField = models.DecimalField(_("Ціна"),
	                                                 max_digits=10,
	                                                 decimal_places=2)
	category: models.ForeignKey = models.ForeignKey(Category,
	                                                on_delete=models.PROTECT,
	                                                related_name="products")
	
	class Meta:
		verbose_name = _("Товар")
		verbose_name_plural = _("Товари")
	
	def __str__(self) -> str:
		return f"{self.name} ({self.price} грн)"


class Sale(models.Model):
	"""
	Unit sales model.
	Fields:
	- product: the product that was sold
	- quantity: the number of units
	- total_price: the total price at the time of sale (price * quantity)
	- created_at: the date/time of sale
	"""
	product: models.ForeignKey = models.ForeignKey(Product,
	                                               on_delete=models.CASCADE,
	                                               related_name="sales")
	quantity: models.PositiveIntegerField = models.PositiveIntegerField(
		_("Кількість"),	default=1)
	total_price: models.DecimalField = models.DecimalField(_("Сума"),
	                                                       max_digits=12,
	                                                       decimal_places=2)
	created_at: models.DateTimeField = models.DateTimeField(_("Створено"),
	                                                        auto_now_add=True)
	
	class Meta:
		verbose_name = _("Продаж")
		verbose_name_plural = _("Продажі")
	
	def __str__(self) -> str:
		return (f"Sale (product={self.product_id}, qty={self.quantity}, "
		        f"total={self.total_price})")
	
	@staticmethod
	def create_for_product(product: Product, quantity: int = 1) -> "Sale":
		"""
		Factory method to create a sale for a product.
		Calculates total_price as product.price * quantity.
		"""
		total = product.price * quantity
		return Sale(product=product, quantity=quantity, total_price=total)
