from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
	"""
	Serializer for Book model
	Used to convert Book objects to JSON and vice versa.
	The 'user' and 'created_at' fields are read-only as
	they are automatically populated.
	"""
	
	class Meta:
		model = Book
		fields = '__all__'
		read_only_fields = ['user', 'created_at']
