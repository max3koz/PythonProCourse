import xml.etree.ElementTree as ET

from typing import List


class Product:
	"""
	The class representing a product.
	Attributes:
		name (str): Product name.
		price (int): Product price.
		quantity (int): Quantity in stock.
	"""
	
	def __init__(self, name: str, price: float, quantity: int) -> None:
		self.name = name
		self.price = price
		self.quantity = quantity
	
	def __repr__(self) -> str:
		return f"{self.name}: {self.quantity} pc(s)"


class ProductManager:
	"""The class for managing a list of products from an XML file."""
	
	def __init__(self):
		self.products: List[Product] = []
		self.tree: ET.ElementTree | None = None
		self.root: ET.Element | None = None
	
	def load_from_file(self, path: str) -> None:
		"""Loads products from XML."""
		self.tree = ET.parse(path)
		self.root = self.tree.getroot()
		self.products.clear()
		
		for item in self.root.findall("product"):
			name = item.find("name").text
			price = float(item.find("price").text)
			quantity = int(item.find("quantity").text)
			self.products.append(Product(name, price, quantity))
	
	def display_product(self) -> None:
		"""Displays names and quantities."""
		print("List of products")
		for product_item in self.products:
			print(f" - {product_item}")
	
	def update_product_quantity(self, name: str, new_quantity: int) -> bool:
		"""Changes the quantity of a product."""
		for product_item in self.root.findall("product"):
			if product_item.find("name").text == name:
				product_item.find("quantity").text = str(new_quantity)
				print(
					f"Quantity of {name} product was changed to {new_quantity}.")
				return True
		print(f"The {name} product is not found")
		return False
	
	def save_to_file(self, path) -> None:
		"""Saves changes to XML."""
		if self.tree:
			self.tree.write(path, encoding="utf-8", xml_declaration=True)
			print(f"Changes were saved in the {path} file.")


manager = ProductManager()

manager.load_from_file("task_05_products_list.xml")
manager.display_product()
manager.update_product_quantity("Milk", 40)
manager.save_to_file("task_05_products_list.xml")
manager.load_from_file("task_05_products_list.xml")
manager.display_product()
