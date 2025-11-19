import logging

import pytest
import requests
from apps.shop.models import Product, CartItem, Order
from assertpy import assert_that
from django.contrib.auth.models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestShopAPIWithAuth:
	"""
	Integration tests for Shop API using live_server and API authentication.
	Covers CRUD for products, cart operations, and orders.
	"""
	
	@pytest.fixture
	def user(self):
		"""Fixture: creates a test user in DB."""
		return User.objects.create_user(username="maksym", password="secret123")
	
	@pytest.fixture
	def session(self, live_server, user):
		"""
		Fixture: creates an authenticated session via API login.
		Uses /api/accounts/login endpoint to obtain token.
		"""
		logger.info("Precondition step 1: "
		            "Creating authenticated session via API login...")
		s = requests.Session()
		login_url = f"{live_server.url}/api/accounts/login"
		payload = {"username": "maksym", "password": "secret123"}
		response = s.post(login_url, json=payload)
		assert response.status_code == 200
		
		token = response.json()["token"]
		logger.info(f"Precondiion step 2: Received token: {token}")
		s.headers.update({"X-CSRFToken": token})
		return s
	
	def test_create_product(self, live_server, session):
		"""Verify that possible to create a new product via POST request."""
		logger.info("Step1: create data for POST request wirh new product data")
		url = f"{live_server.url}/api/shop/products/"
		payload = {
			"name": "Laptop",
			"description": "Gaming laptop",
			"price": 1500.00,
			"stock": 10
		}
		
		logger.info("Step 2: send POST request anf verify status code 201")
		response = session.post(url, json=payload)
		assert_that(response.status_code).is_equal_to(201)  # 👈 створення → 201
		
		logger.info("Step 3: verify responde data")
		data = response.json()
		
		logger.info("Step 4: verify that new product in the database")
		assert_that(data["name"]).is_equal_to("Laptop")
		assert_that(Product.objects.filter(name="Laptop").exists()).is_true()
	
	def test_update_product(self, live_server, session):
		"""Verify that possible to update an existing product via PUT request."""
		logger.info("Step 1: create dats with updated data for product")
		product = Product.objects.create(name="Old", description="Old desc",
		                                 price=100, stock=5)
		url = f"{live_server.url}/api/shop/products/{product.id}"
		payload = {"name": "New", "description": "New desc", "price": 200,
		           "stock": 10}
		
		logger.info("Step 2: verify the status cod 200")
		response = session.put(url, json=payload)
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 3: verify that data was changed in th database")
		product.refresh_from_db()
		assert_that(product.name).is_equal_to("New")
		assert_that(product.price).is_equal_to(200)
	
	def test_list_products(self, live_server, session):
		"""Verify that possible to get the list all products via GET request."""
		logger.info("Step 1: create test data list in the database")
		Product.objects.create(name="Phone", description="Smartphone",
		                       price=500, stock=20)
		Product.objects.create(name="Tablet", description="Android tablet",
		                       price=300, stock=15)
		
		logger.info("Step 2: send GET request and verify that the status code 200")
		url = f"{live_server.url}/api/shop/products/"
		response = session.get(url)
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step3: verify the list od products ")
		data = response.json()
		names = [p["name"] for p in data]
		assert_that(names).contains("Phone", "Tablet")
	
	def test_get_nonexistent_product(self, live_server, session):
		"""Verify that impossible to retrieve a non-existent product."""
		url = f"{live_server.url}/api/shop/products/9999"
		response = session.get(url)
		assert_that(response.status_code).is_equal_to(404)
	
	def test_delete_product(self, live_server, session):
		"""Verify that possible to delete an existing product."""
		logger.info("Step 1: create test data")
		product = Product.objects.create(name="ToDelete", description="Temp",
		                                 price=50, stock=1)
		
		logger.info("Step 2: delete product and verify that the product was "
		            "deleted fron database")
		url = f"{live_server.url}/api/shop/products/{product.id}"
		response = session.delete(url)
		assert_that(response.status_code).is_equal_to(200)
		assert_that(Product.objects.filter(id=product.id).exists()).is_false()
	
	def test_add_to_cart(self, live_server, session, user):
		"""Verify that possible to add product to cart via POST request."""
		logger.info("Step 1: create test data")
		product = Product.objects.create(name="Mouse",
		                                 description="Wireless mouse", price=50,
		                                 stock=100)
		
		logger.info("Step 2: added product to the cart and verify that "
		            "the product was adde  to the cart")
		url = f"{live_server.url}/api/shop/cart/"
		payload = {"product_id": product.id, "quantity": 2}
		response = session.post(url, json=payload)
		assert_that(response.status_code).is_equal_to(201)
		
		assert_that(CartItem.objects.filter(user=user,
		                                    product=product).exists()).is_true()
	
	def test_add_nonexistent_product_to_cart(self, live_server, session):
		"""Verify that impossible to add non-existent product to cart."""
		url = f"{live_server.url}/api/shop/cart/"
		payload = {"product_id": 9999, "quantity": 1}
		response = session.post(url, json=payload)
		assert_that(response.status_code).is_equal_to(404)
	
	def test_create_order(self, live_server, session, user):
		"""VeRify that possible to create order from cart via POST request."""
		logger.info("Step 1: create test data")
		product = Product.objects.create(name="Keyboard",
		                                 description="Mechanical keyboard",
		                                 price=120, stock=50)
		CartItem.objects.create(user=user, product=product, quantity=1)

		logger.info("Step 2: create  order")
		url = f"{live_server.url}/api/shop/orders/"
		response = session.post(url)
		assert_that(response.status_code).is_equal_to(201)
		
		logger.info("Step 3: verify that the order is exist")
		data = response.json()
		assert_that(data["status"]).is_equal_to("pending")
		assert_that(Order.objects.filter(user=user).exists()).is_true()
	
	def test_create_order_empty_cart(self, live_server, session, user):
		"""Verify that impossible to create order from cart via POST request."""
		logger.info("Step1: send POST request")
		url = f"{live_server.url}/api/shop/orders/"
		response = session.post(url)
		assert_that(response.status_code).is_equal_to(201)
		
		logger.info("Step 2: verify that status is pending")
		data = response.json()
		assert_that(data["status"]).is_equal_to("pending")
		
		logger.info("Step 3: verify that order was created without OrderItem")
		order = Order.objects.get(user=user)
		assert_that(order.items.count()).is_equal_to(0)
	
	def test_update_order_status(self, live_server, session, user):
		"""Test: update order status via PUT request."""
		logger.info("step 1: create the order")
		order = Order.objects.create(user=user, status="pending")
		url = f"{live_server.url}/api/shop/orders/{order.id}"
		
		logger.info("Step 2: send POST request")
		response = session.put(url, json={"status": "shipped"})
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 2: verify updated order status")
		order.refresh_from_db()
		assert_that(order.status).is_equal_to("shipped")
		
	def test_update_nonexistent_order_status(self, live_server, session):
		"""Verify that impossible to update nonexistent order status """
		logger.info("Step 1: Send PUT requst ")
		url = f"{live_server.url}/api/shop/orders/9999"
		response = session.put(url, json={"status": "shipped"})
		
		logger.info("Step 2: verify that response status is 4014")
		assert_that(response.status_code).is_equal_to(404)
