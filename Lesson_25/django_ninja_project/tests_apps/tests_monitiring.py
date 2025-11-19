import logging

import pytest
import requests
from apps.monitoring.models import Server, Metric
from assertpy import assert_that
from django.contrib.auth.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestMonitoringAPI:
	"""
	Integration tests for Server Monitoring API.
	Covers CRUD for servers and metrics.
	"""
	
	@pytest.fixture
	def user(self) -> User:
		"""Fixture: creates a test user in DB."""
		return User.objects.create_user(username="maksym", password="secret123")
	
	@pytest.fixture
	def session(self, live_server, user):
		"""
		Fixture: creates an authenticated session via API login.
		"""
		logger.info("Precondition step 1: Logging in user via API...")
		s = requests.Session()
		login_url = f"{live_server.url}/api/accounts/login"
		payload = {"username": "maksym", "password": "secret123"}
		response = s.post(login_url, json=payload)
		assert response.status_code == 200
		token = response.json()["token"]
		
		logger.info("Precondition step 2: Adding token to headers...")
		s.headers.update({"X-CSRFToken": token})
		return s
	
	# ------------------ Servers ------------------
	def test_create_server(self, live_server, session):
		"""Verify that possible to create a new server."""
		logger.info("Step 1: create the server data")
		url = f"{live_server.url}/api/monitoring/servers/"
		payload = {"name": "Server1", "ip_address": "192.168.0.10",
		           "status": "online"}
		
		logger.info("Step 2: Sending POST request to create server...")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: Verifying response status")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(Server.objects.filter(name="Server1").exists()).is_true()
	
	def test_create_server_unauthorized(self, live_server):
		"""Verify that impossible to create server without authentication."""
		logger.info("Step 1: create the server data")
		url = f"{live_server.url}/api/monitoring/servers/"
		payload = {"name": "NoAuth", "ip_address": "192.168.0.20",
		           "status": "online"}
		
		logger.info("Step 2: Sending POST request to create server...")
		response = requests.post(url, json=payload)
		
		logger.info("Step 3: Verify that the status code 401")
		assert_that(response.status_code).is_equal_to(401)
	
	def test_list_servers(self, live_server, session):
		"""Verify that possible to get list all servers."""
		logger.info("Step 1: create the server data list")
		Server.objects.create(name="SrvA", ip_address="10.0.0.1",
		                      status="online")
		Server.objects.create(name="SrvB", ip_address="10.0.0.2",
		                      status="offline")
		url = f"{live_server.url}/api/monitoring/servers/"
		
		logger.info("Step 2: sending GET request to list servers")
		response = session.get(url)
		
		logger.info("Step 3: Checking response contains servers.")
		assert_that(response.status_code).is_equal_to(200)
		names = [s["name"] for s in response.json()]
		assert_that(names).contains("SrvA", "SrvB")
	
	def test_get_server(self, live_server, session):
		"""Verify that possible get a single server by ID."""
		logger.info("Step 1: create the server data")
		server = Server.objects.create(name="SrvX", ip_address="10.0.0.3",
		                               status="online")
		url = f"{live_server.url}/api/monitoring/servers/{server.id}"
		
		logger.info("Step 2: Sending GET request to retrieve server")
		response = session.get(url)
		
		logger.info("Step 3: Checking response contains server.")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.json()["name"]).is_equal_to("SrvX")
	
	def test_get_nonexistent_server(self, live_server, session):
		"""Verify that impossible to retrieve non-existent server."""
		logger.info("Step 1: create the server data")
		url = f"{live_server.url}/api/monitoring/servers/9999"
		
		logger.info("Step 2: Sending GET request to retrieve server")
		response = session.get(url)
		
		logger.info("Step 3: Verify that the status code 404")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_update_server(self, live_server, session):
		"""Verify that possible to update an existing server."""
		logger.info("Step 1: create the server data")
		server = Server.objects.create(name="SrvOld", ip_address="10.0.0.4",
		                               status="offline")
		url = f"{live_server.url}/api/monitoring/servers/{server.id}"
		payload = {"name": "SrvNew", "ip_address": "10.0.0.4",
		           "status": "online"}
		
		logger.info("Step 2: Sending PUT request to update server")
		response = session.put(url, json=payload)
		
		logger.info("Step 3: Checking response contains updated servers.")
		assert_that(response.status_code).is_equal_to(200)
		server.refresh_from_db()
		assert_that(server.name).is_equal_to("SrvNew")
		assert_that(server.status).is_equal_to("online")
	
	def test_delete_server(self, live_server, session):
		"""Verify that possible to delete a server."""
		logger.info("Step 1: create the server data")
		server = Server.objects.create(name="SrvDel", ip_address="10.0.0.5",
		                               status="offline")
		url = f"{live_server.url}/api/monitoring/servers/{server.id}"
		
		logger.info("Step 2: sending DELETE request to remove server")
		response = session.delete(url)
		
		logger.info("Step 3: Checking response doesn't contain deleted servers.")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(Server.objects.filter(id=server.id).exists()).is_false()
	
	# ------------------ Metrics ------------------
	def test_add_metric(self, live_server, session):
		"""Verify that possible to add metrics for a server.
		"""
		logger.info("Step 1: create the metric data")
		server = Server.objects.create(name="SrvMetric", ip_address="10.0.0.6",
		                               status="online")
		url = f"{live_server.url}/api/monitoring/metrics/"
		payload = {"server_id": server.id, "cpu_usage": 50.0,
		           "memory_usage": 40.0, "load": 1.2}
		
		logger.info("Step 2: Sending POST request to add metrics")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: Checking response contains metric.")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(Metric.objects.filter(server=server).exists()).is_true()
	
	def test_add_metric_unauthorized(self, live_server, user):
		"""Verify that impossible to add metrics without authentication."""
		logger.info("Step 1: create the metric data")
		server = Server.objects.create(name="SrvNoAuth", ip_address="10.0.0.8",
		                               status="online")
		url = f"{live_server.url}/api/monitoring/metrics/"
		payload = {"server_id": server.id, "cpu_usage": 95.0,
		           "memory_usage": 90.0, "load": 2.0}
		
		logger.info("Step 2: Sending POST request to add metrics")
		response = requests.post(url, json=payload)
		
		logger.info("Step 3: Verify that the status code 401")
		assert_that(response.status_code).is_equal_to(401)
	
	def test_list_metrics(self, live_server, session):
		"""Verify that possible to get list metrics for a server."""
		logger.info("Step 1: create the metric data list")
		server = Server.objects.create(name="SrvMetric2", ip_address="10.0.0.7",
		                               status="online")
		Metric.objects.create(server=server, cpu_usage=20.0, memory_usage=30.0,
		                      load=0.5)
		Metric.objects.create(server=server, cpu_usage=70.0, memory_usage=60.0,
		                      load=1.5)
		url = f"{live_server.url}/api/monitoring/metrics/{server.id}"
		
		logger.info("Step 2: Sending GET request to list metrics")
		response = session.get(url)
		
		logger.info("Step 3: Checking response contains metrics.")
		assert_that(response.status_code).is_equal_to(200)
		metrics = response.json()
		assert_that(len(metrics)).is_equal_to(2)
	
	def test_list_metrics_nonexistent_server(self, live_server, session):
		"""Verify that im possible to get list metrics for non-existent server."""
		logger.info("Step 1: create the metric data list")
		url = f"{live_server.url}/api/monitoring/metrics/9999"

		logger.info("Step 2: sending GET request to list metrics")
		response = session.get(url)
		
		logger.info("Step 3: Verify that the status code 404")
		assert_that(response.status_code).is_equal_to(404)
