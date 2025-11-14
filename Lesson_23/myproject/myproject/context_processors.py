from typing import Dict

from django.http import HttpRequest


def global_data(request: HttpRequest) -> Dict[str, str]:
	"""
	A context processor that adds global variables to templates.
	Adds: site_name: Site name and user_ip: User IP address from request metadata
	Args: request (HttpRequest): Current HTTP request.
	Returns: Dict[str, str]: Dictionary with global variables for the template.
	"""
	return {
		'site_name': 'My Awesome Site',
		'user_ip': request.META.get('REMOTE_ADDR', '')
	}
