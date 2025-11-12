from typing import Dict, Any

from django.views.generic import TemplateView
from rest_framework import viewsets

from .models import CustomModel
from .serializers import CustomModelSerializer


class CustomView(TemplateView):
	"""
	Class-based View for rendering the template 'custom.html'.
	Adds the message 'Hello from CBV!' to the template context.
	"""
	template_name = 'custom.html'
	
	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
		"""
		Forms a context for the template.
		Args: **kwargs (Any): Additional context arguments.
		Returns: Dict[str, Any]: Context with message.
		"""
		context = super().get_context_data(**kwargs)
		context['message'] = 'Hello from CBV!'
		return context


class CustomModelViewSet(viewsets.ModelViewSet):
	"""ViewSet for CustomModel.	Allows full CRUD via REST API."""
	queryset = CustomModel.objects.all()
	serializer_class = CustomModelSerializer
