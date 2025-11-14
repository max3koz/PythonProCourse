from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import CustomModel, RelatedModel


class RelatedInline(admin.TabularInline):
	"""
	Inline editor for the RelatedModel model that is related to the CustomModel.
	Displays 1 empty line for creating a new object.
	"""
	model = RelatedModel
	extra = 1


@admin.register(CustomModel)
class CustomModelAdmin(admin.ModelAdmin):
	"""
	CustomModel admin:
	- Displays the 'name' field in the list
	- Adds a filter by 'name'
	- Adds an inline editor for RelatedModel
	- Adds the 'make_uppercase' action
	"""
	list_display = ('name',)
	list_filter = ('name',)
	actions = ['make_uppercase']
	inlines = [RelatedInline]
	
	def make_uppercase(self, request: HttpRequest,
	                   queryset: QuerySet[CustomModel]) -> None:
		"""
		Converts the 'name' value of the selected objects to uppercase.
		Args:
		- request (HttpRequest): Request from the admin;
		- queryset (QuerySet[CustomModel]): Selected model objects.
		"""
		for obj in queryset:
			obj.name = obj.name.upper()
			obj.save()
