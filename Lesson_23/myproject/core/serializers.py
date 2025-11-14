from rest_framework import serializers

from .models import CustomModel


class CustomModelSerializer(serializers.ModelSerializer):
	"""
	Serializer for the CustomModel model.
	Includes all model fields:
	- name: text field, automatically saved in uppercase
	- data: JSON field with arbitrary structure
	"""
	
	class Meta:
		model = CustomModel
		fields = '__all__'
