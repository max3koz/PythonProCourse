from django.apps import AppConfig


class CoreConfig(AppConfig):
	"""
	The 'core' application configuration.
	Sets the default autoincrement field type and application name for Django.
	"""
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'core'
