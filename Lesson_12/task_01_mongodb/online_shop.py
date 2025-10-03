from datastore import OnlineStore

store = OnlineStore()

store.products.delete_many({})
store.orders.delete_many({})

store.add_product("Laptop", 1200, "Computers", 10)
store.add_product("E-book", 20, "Devices", 50)
store.add_product("Headset", 80, "Accessories", 25)

store.add_order(
	order_id="ORD001",
	customer="Customer_1",
	items=[{"product": "Laptop", "quantity": 1},
	       {"product": "E-book", "quantity": 2}],
	total=1240
)

store.add_order(
	order_id="ORD002",
	customer="Customer_2",
	items=[{"product": "Headset", "quantity": 1}],
	total=80
)

store.update_stock("Headset", -1)

store.delete_unavailable_products()

# --- Receiving orders in 20 days ---
recent_orders = store.get_recent_orders(days=20)
for order in recent_orders:
	print(order)

print("Sold Out:")
print(store.total_products_sold())

print("Customer_1 expenses:")
print(store.total_spent_by_customer("Customer_1"))

store.create_category_index()
