from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from pymongo import MongoClient, ASCENDING


class OnlineStore:
	"""
	The class for managing an online store based on MongoDB.
	It contains CRUD operations for products and orders.
	"""
	
	def __init__(self, uri="mongodb://localhost:27017/",
	             db_name="online_store"):
		"""
		Initializes a connection to MongoDB and creates links to collections.
		"""
		self.client = MongoClient(uri)
		self.db = self.client[db_name]
		self.products = self.db.products
		self.orders = self.db.orders
	
	# --- CRUD product operations ---
	def add_product(self, name: str, price: float, category: str,
	                stock: str) -> None:
		"""The function adds a new product to the products collection."""
		self.products.insert_one({
			"name": name,
			"price": price,
			"category": category,
			"stock": stock
		})
	
	def delete_unavailable_products(self):
		"""The function removes products that are out of stock (stock <= 0)."""
		self.products.delete_many({"stock": {"$lte": 0}})
	
	def update_stock(self, product_name: str, quantity_change: int) -> None:
		"""The function changes the quantity of goods in stock."""
		self.products.update_one(
			{"name": product_name},
			{"$inc": {"stock": quantity_change}}
		)
	
	# --- CRUD order operations ---
	def add_order(self, order_id: str, customer: str,
	              items: List[Dict[str, Any]], total: float,
	              date: Optional[datetime] = None) -> None:
		"""The function adds a new order to the orders collection."""
		self.orders.insert_one({
			"orderId": order_id,
			"customer": customer,
			"items": items,
			"total": total,
			"date": date or datetime.utcnow()
		})
	
	def get_recent_orders(self, days: int = 30) -> List[Dict[str, Any]]:
		"""The function returns a list of orders for the last N days."""
		cutoff = datetime.utcnow() - timedelta(days=days)
		return list(self.orders.aggregate([{"$match": {
			"date": {"$gte": cutoff}}},
			{"$addFields": {
				"date": {"$dateToString": {"format": "%d-%m-%Y %H:%M:%S",
				                           "date": "$date"}
				         }
				}}
		]))
	
	def total_products_sold(self) -> List[Dict[str, Any]]:
		"""The function returns the total number of units sold for each product."""
		return list(self.orders.aggregate([
			{"$unwind": "$items"},
			{"$group": {"_id": "$items.product",
			            "totalSold": {"$sum": "$items.quantity"}
			            }}
		]))
	
	def total_spent_by_customer(self, customer_name: str) -> List[
		Dict[str, Any]]:
		"""The function returns the total amount of the customer's expenses."""
		return list(self.orders.aggregate([
			{"$match": {"customer": customer_name}},
			{"$group": {"_id": "$customer", "totalSpent": {"$sum": "$total"}
			            }}
		]))
	
	# --- Indexing ---
	def create_category_index(self) -> str:
		"""
		The function creates an index on the category field
		in the products collection.
		"""
		self.products.create_index([("category", ASCENDING)])
