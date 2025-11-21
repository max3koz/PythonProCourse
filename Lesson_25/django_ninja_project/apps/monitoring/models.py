from django.db import models


class Server(models.Model):
	"""Represents a monitored server."""
	name: str = models.CharField(max_length=100, unique=True)
	ip_address: str = models.GenericIPAddressField(unique=True)
	status: str = models.CharField(max_length=10,
	                               choices=[("online", "Online"),
	                                        ("offline", "Offline")],
	                               default="offline")
	created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
	
	def __str__(self) -> str:
		return f"{self.name} ({self.status})"


class Metric(models.Model):
	"""Represents monitoring metrics for a server."""
	server: Server = models.ForeignKey(Server, on_delete=models.CASCADE,
	                                   related_name="metrics")
	cpu_usage: float = models.FloatField()
	memory_usage: float = models.FloatField()
	load: float = models.FloatField()
	timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)
	
	def __str__(self) -> str:
		return f"Metrics for {self.server.name} at {self.timestamp}"
