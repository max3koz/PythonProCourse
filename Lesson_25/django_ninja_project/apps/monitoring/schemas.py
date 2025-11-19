from ninja import Schema
from datetime import datetime


class ServerIn(Schema):
    name: str
    ip_address: str
    status: str


class ServerOut(Schema):
    id: int
    name: str
    ip_address: str
    status: str
    created_at: datetime


class MetricIn(Schema):
    server_id: int
    cpu_usage: float
    memory_usage: float
    load: float


class MetricOut(Schema):
    id: int
    server_id: int
    cpu_usage: float
    memory_usage: float
    load: float
    timestamp: datetime
