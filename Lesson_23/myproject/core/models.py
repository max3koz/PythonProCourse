from typing import Dict, Any

from django.db import models


class UpperTextField(models.CharField):
	"""
	A custom text field that automatically saves values ​​in uppercase.
	Inherits the standard CharField, but modifies the prepared value before saving.
	"""
	
	def get_prep_value(self, value: Any) -> str:
		"""
		Returns the value in uppercase before saving to the database.
		Args: value (Any): Input value.
		Returns:str: Value in uppercase.
		"""
		return str(value).upper()


class CustomModel(models.Model):
	"""
	Basic model with two fields:
	- name: text stored in uppercase
	- data: JSON structure with arbitrary keys and values
	"""
	name: str = UpperTextField(max_length=100)
	data: Dict[str, Any] = models.JSONField(default=dict)
	
	def get_stats(self) -> Dict[str, Any]:
		"""
		Returns statistics on the JSON field 'data'.
		Returns: Dict[str, Any]: Number of keys and list of values.
		"""
		return {
			"keys": len(self.data.keys()),
			"values": list(self.data.values())
		}


class RelatedModel(models.Model):
	"""
	A model related to a CustomModel via a ForeignKey.
	Stores an additional text value.
	"""
	custom: CustomModel = models.ForeignKey(CustomModel,
	                                        related_name='related',
	                                        on_delete=models.CASCADE)
	value: str = models.CharField(max_length=100)
