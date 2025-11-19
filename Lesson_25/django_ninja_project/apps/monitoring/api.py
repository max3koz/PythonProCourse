from ninja import Router
from ninja.responses import Response
from django.shortcuts import get_object_or_404
from .models import Server, Metric
from .schemas import ServerIn, ServerOut, MetricIn, MetricOut

monitoring_router = Router(tags=["monitoring"])


# ------------------ Servers ------------------
@monitoring_router.post("/servers/", response=ServerOut)
def create_server(request, payload: ServerIn) -> Response:
    """Create a new server. Requires authentication."""
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=401)
    server = Server.objects.create(**payload.dict())
    return Response(ServerOut.from_orm(server), status=201)


@monitoring_router.get("/servers/", response=list[ServerOut])
def list_servers(request):
    """Retrieve all servers."""
    return Server.objects.all()


@monitoring_router.get("/servers/{server_id}", response=ServerOut)
def get_server(request, server_id: int):
    """Retrieve a single server by ID."""
    return get_object_or_404(Server, id=server_id)


@monitoring_router.put("/servers/{server_id}", response=ServerOut)
def update_server(request, server_id: int, payload: ServerIn):
    """Update an existing server. Requires authentication."""
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=401)
    server = get_object_or_404(Server, id=server_id)
    for attr, value in payload.dict().items():
        setattr(server, attr, value)
    server.save()
    return server


@monitoring_router.delete("/servers/{server_id}")
def delete_server(request, server_id: int):
    """Delete a server. Requires authentication."""
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=401)
    server = get_object_or_404(Server, id=server_id)
    server.delete()
    return {"success": True}


# ------------------ Metrics ------------------
@monitoring_router.post("/metrics/", response=MetricOut)
def add_metric(request, payload: MetricIn) -> Response:
    """Add metrics for a server. Requires authentication."""
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required"}, status=401)
    server = get_object_or_404(Server, id=payload.server_id)
    metric = Metric.objects.create(server=server, **payload.dict(exclude={"server_id"}))
    # Critical alert check
    if metric.cpu_usage > 90 or metric.memory_usage > 90:
        # Here you could integrate email/Slack notifications
        return Response({"detail": "Critical threshold reached"}, status=201)
    return Response(MetricOut.from_orm(metric), status=201)


@monitoring_router.get("/metrics/{server_id}", response=list[MetricOut])
def list_metrics(request, server_id: int):
    """Retrieve all metrics for a specific server."""
    server = get_object_or_404(Server, id=server_id)
    return server.metrics.all()
