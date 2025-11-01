from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
	"""ViewSet for books control"""
	
	queryset = Book.objects.all().order_by('-created_at')
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [DjangoFilterBackend, filters.SearchFilter]
	filterset_fields = ['author', 'genre', 'publication_year']
	search_fields = ['title']
	
	def perform_destroy(self, instance: Book) -> None:
		"""Allows only the administrator to delete books"""
		if not self.request.user.is_staff:
			raise PermissionDenied("Only an administrator can delete books.")
		instance.delete()
	
	def perform_create(self, serializer):
		"""
		Called when a new object is created via the API.
		Automatically saves the model object, binding it to the currently
		authenticated user.
		"""
		serializer.save(user=self.request.user)
